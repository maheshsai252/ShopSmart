import os
import pandas as pd
import json
from helpers.call_gen_ai import call_gemini_api


def update_ratings_product(**context):
    task_instance = context['task_instance']
    file = task_instance.xcom_pull(task_ids='clean_reviews_task')
    filename = file.split("_cleaned.csv")[0]

    # file = "mens_clothing_reviews_cleaned.csv"
    cleaned_file = f'{filename}_ratings.csv'
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    file_path = os.path.join(resources, file)
    cleaned_file_path = os.path.join(resources, cleaned_file)
    if os.path.exists(cleaned_file_path):
        return cleaned_file
    df = pd.read_csv(file_path)
    unique_products = df['asin'].unique()
    products = []
    rows = len(unique_products)
    i=0
    paused = None
    while i<rows:
        if paused:
            i=paused
        current_product = unique_products[i]
        reviews_df = df[df['asin'] == current_product]
        product={}
        product['asin'] = current_product
        context=""
        product['rating'] = reviews_df['rating'].mean()
        if not product['rating']:
            product['rating'] = 0
        products.append(product)
        i+=1

    sdf = pd.DataFrame(products)
    sdf.to_csv(cleaned_file_path, index=False)
    
    return cleaned_file