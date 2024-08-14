import os
import pandas as pd
import json
from helpers.call_gen_ai import call_gemini_api

instruction = """
Give a concise summary for the below reviews given by users for the product in the form 
{"summary": ...}.
\n\nReviews:\n"""

def summarise_reviews(**context):
    task_instance = context['task_instance']
    file = task_instance.xcom_pull(task_ids='clean_reviews_task')
    filename = file.split("_cleaned.csv")[0]

    # file = "mens_clothing_reviews_cleaned.csv"
    cleaned_file = f'{filename}_summaries.csv'
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
        batch_size = 20
        num_reviews = len(reviews_df)
        for j in range(0, num_reviews, batch_size):
            batch_reviews = reviews_df.iloc[j:j+batch_size]
            context = ""
            for _, review in batch_reviews.iterrows():
                context += str(review['summary'])
                context += str(review['reviewtext'])
            try:
                generated_text = call_gemini_api(instruction+context)
            except:
                paused = i 
                continue               
            if generated_text!="UNSAFE": 
                try:
                    product["summary"] = json.loads(generated_text.strip())["summary"]
                except:
                    product['summary'] = ""
            else:
                product['summary'] = ""
            paused = None
            products.append(product)
        i+=1

    sdf = pd.DataFrame(products)
    sdf = sdf.fillna('')
    sdf.to_csv(cleaned_file_path, index=False)
    
    return cleaned_file