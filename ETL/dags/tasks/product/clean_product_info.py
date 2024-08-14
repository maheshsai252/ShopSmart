import os
import pandas as pd
def clean_product_info(**context):
    file = "men_watches_data.csv"
    filename = file.split("_data.csv")[0]
    cleaned_file = f'{filename}_cleaned.csv'
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    file_path = os.path.join(resources, file)
    cleaned_file_path = os.path.join(resources, cleaned_file)
    df = pd.read_csv(file_path)

    # Fill NA values with spaces
    df = df.fillna(' ')

    # Perform additional cleaning tasks (add your cleaning logic here)

    # Example: Convert column names to lowercase
    df.columns = df.columns.str.lower()

    # Example: Remove leading and trailing whitespaces from string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Example: Drop rows with any missing values
    df = df.dropna()

    df.to_csv(cleaned_file_path, index=False)
    
    return cleaned_file