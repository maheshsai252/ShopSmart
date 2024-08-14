import os
import pandas as pd
def clean_reviews(**context):
    file = "men_watches_reviews_data.csv"
    filename = file.split("_data.csv")[0]
    cleaned_file = f'{filename}_cleaned.csv'
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    file_path = os.path.join(resources, file)
    cleaned_file_path = os.path.join(resources, cleaned_file)
    df = pd.read_csv(file_path)

    df = df.fillna(' ')

    df.columns = df.columns.str.lower()

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.fillna('')
    df = df.dropna()

    df.to_csv(cleaned_file_path, index=False)
    
    return cleaned_file