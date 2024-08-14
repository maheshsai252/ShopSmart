from pydantic import BaseModel, Field, validator
import pandas as pd
import os

class Product(BaseModel):
    title: str
    features: str
    description: str
    asin: str
    imageurl: str
    imageurlhighres: str
    category: str

class ReviewSummary(BaseModel):
    asin: str
    summary: str

class ProductSummary(BaseModel):
    asin: str
    title: str
    summary: str
def validate_data(csv_filename):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')  # Create a folder named 'downloaded_files' in the DAG folder
    # res_path = os.path.join(res_path, str(run_id))

    c1 = os.path.join(res_path,csv_filename)
    df = pd.read_csv(c1)
    try:
        for _, row in df.iterrows():
            instance = Product(
                title = row['title'],
                features= row['features'],
                description= row['description'],
                asin= row['asin'],
                imageurl= row['imageurl'],
                imageurlhighres= row['imageurlhighres'],
                category= row['category']
            )
    except Exception as e:
        print(str(e))
    return csv_filename
def validate_review_summaries(csv_filename):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    c1 = os.path.join(res_path,csv_filename)
    df = pd.read_csv(c1)
    try:
        for _, row in df.iterrows():
            instance = ReviewSummary(
                asin = row['asin'],
                summary = row['summary']
            )
    except Exception as e:
        print(str(e))
    return csv_filename

def validate_product_summaries(csv_filename):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    c1 = os.path.join(res_path,csv_filename)
    df = pd.read_csv(c1)
    try:
        for _, row in df.iterrows():
            instance = ProductSummary(
                asin = row['asin'],
                title = row['title'],
                summary = row['summary']
            )
    except Exception as e:
        print(str(e))
    return csv_filename