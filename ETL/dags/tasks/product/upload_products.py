import os
import pandas as pd
import re
from helpers.pinecone_helper_functions import generate_embedding, store_in_pinecone
from helpers.upload_to_snowflake_helper import upload_products_to_snowflake, upload_product_summaries_to_snowflake
def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)
def upload_products(**context):
    task_instance = context['task_instance']
    file = task_instance.xcom_pull(task_ids='summarise_product_info')
    cat = file.split("_summaries.csv")[0]
    # file = "mens_clothing_summaries.csv"
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    file_path = os.path.join(resources, file)
    df = pd.read_csv(file_path)
    chunk_embeddings = []
    chunk_ids = []
    meta = []
    for _, sample in df.iterrows():
        text=sample['summary']
        text+=sample['title']
        try:
            embedding = generate_embedding(text)
            chunk_embeddings.append(embedding)
            id = remove_non_ascii(f"{sample['asin']}_product_summary")
            chunk_ids.append(id)
            meta_cur ={'summary': sample['summary'], 'asin': sample['asin']}
            meta.append(meta_cur)
        except:
            continue

    print(cat)
    store_in_pinecone(chunk_embeddings, chunk_ids, meta, namespace=cat)

def upload_products_summaries_to_snowflake_function(**context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='summarise_product_info')
    # filename = data.split("_cleaned.csv")[0]
    return upload_product_summaries_to_snowflake(data)

def upload_products_to_snowflake_function(**context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='clean_product_info')
    # filename = data.split("_cleaned.csv")[0]
    return upload_products_to_snowflake(data)