import os
import pandas as pd
import re
from collections import defaultdict
from helpers.pinecone_helper_functions import generate_embedding, store_in_pinecone
from helpers.upload_to_snowflake_helper import upload_reviews_to_snowflake, upload_ratings_reviews_to_snowflake

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)
def upload_reviews(**context):
    task_instance = context['task_instance']
    file = task_instance.xcom_pull(task_ids='summarise_reviews_task')
    cat = file.split("_reviews_summaries.csv")[0]
    # file = "mens_clothing_reviews_summaries.csv"
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    file_path = os.path.join(resources, file)
    df = pd.read_csv(file_path)
    chunk_embeddings = []
    chunk_ids = []
    meta = []
    id_mapper = defaultdict(int)
    for idx, sample in df.iterrows():
        text=sample['summary']
        print(idx, text)
        if str(text) == 'nan':
            continue
        embedding = generate_embedding(text)
        chunk_embeddings.append(embedding)
        id_mapper[sample['asin']] = id_mapper[sample['asin']] + 1
        id = remove_non_ascii(f"{sample['asin']}_review_summary_{id_mapper[sample['asin']]}")
        chunk_ids.append(id)
        meta_cur ={'summary': sample['summary'], 'asin': sample['asin']}
        meta.append(meta_cur)

    store_in_pinecone(chunk_embeddings, chunk_ids, meta, namespace=cat)

def upload_reviews_to_snowflake_function(**context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='summarise_reviews_task')
    return upload_reviews_to_snowflake(data)

def upload_ratings_reviews_to_snowflake_function(**context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='update_ratings_task')
    return upload_ratings_reviews_to_snowflake(data)

