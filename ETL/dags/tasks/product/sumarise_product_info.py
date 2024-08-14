import os
import pandas as pd
import json
from helpers.call_gen_ai import call_gemini_api
instruction = """
Give a concise summary for the below description of the product in the form 
Don't include anything other than summary in your response.
\n\nProduct Info:\n
"""

def summarise_product_info(**context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='clean_product_info')
    # file = "mens_clothing_data_cleaned.csv"
    filename = data.split("_cleaned.csv")[0]
    cleaned_file = f'{filename}_summaries.csv'
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    file_path = os.path.join(resources, data)
    cleaned_file_path = os.path.join(resources, cleaned_file)
    df = pd.read_csv(file_path)
    if os.path.exists(cleaned_file_path):
        return cleaned_file
    products = []
    rows = len(df)
    i=0
    paused = None
    while i<rows:
        if paused:
            i=paused
        sample = df.iloc[i]
        product={}
        product['asin'] = sample['asin']
        title = sample['title']
        product['title'] = title
        features = sample['features']
        description = sample['description']
        if description and features:
            context = f"""Description:\n{description}\nFeatures:{features}"""
        elif description:
            context = description
        elif features:
            context = features
        else:
            context = ""
        try:
            generated_text = call_gemini_api(instruction+context)
        except Exception as e:
            print(str(e))
            paused = i 
            continue               
        if generated_text!="UNSAFE": 
            product["summary"] = generated_text.strip()
        paused = None
        products.append(product)
        i+=1

    sdf = pd.DataFrame(products)
    sdf.to_csv(cleaned_file_path, index=False)
    
    return cleaned_file