from typing import List
import snowflake.connector
import os
from collections import defaultdict
snowflake_config = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': 'Marketplace',
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}
def get_user_cart_products(user_id) -> List[dict]:
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()
    query = f"SELECT distinct product_id FROM userswishlist WHERE user_id = {user_id}"
    cursor.execute(query)
    asins = cursor.fetchall()
    asins = [str(asin[0]) for asin in asins]
    asins= ",".join(f"'{asin}'" for asin in asins)
    print(asins)
    if asins:
        query = f"SELECT distinct title, features, description, imageURLHighRes,category, asin FROM Products WHERE asin IN ({asins})"
        print(query)
        cursor.execute(query)
        # cursor.execute(f"SELECT title,features,description,imageURLHighRes FROM Products WHERE asin in '%{asins}%'")
    data = cursor.fetchall()
    if asins:
        query = f"SELECT summary,asin FROM ProductsSummaries WHERE asin IN ({asins})"
        cursor.execute(query)
        # cursor.execute(f"SELECT title,features,description,imageURLHighRes FROM Products WHERE asin in '%{asins}%'")
    summary_data = cursor.fetchall()
    cursor.close()
    conn.close()

    
    summaries = {row[-1]: row[:-1] for row in summary_data}

    # Update the products list with the fetched data
    products = []
    existing_asins = []
    for row in data:
        asin = row[-1]
        print(asin)
        if asin in existing_asins:
            continue
        else:
            existing_asins.append(asin)
        product = {"asin": asin}
        title, features, description, imageURLHighRes, category = row[:-1]
        product.update({
                'title': title,
                'imageURLHighRes': imageURLHighRes,
                'category': category,
                'summary': summaries[asin][0] if len(summaries[asin])>0 else summaries[asin][0]
            })
        products.append(product)
    print(len(products))
    return products
def get_review_summaries(asins):
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()
    sasins= ",".join(f"'{asin}'" for asin in asins)
    query = f"SELECT summary,asin FROM PRODUCTSREVIEWSUMMARIES WHERE asin IN ({sasins})"
    cursor.execute(query)
    summary_data = cursor.fetchall()
    print("reciew summary", summary_data)
    ret_summary = defaultdict(str)
    for s in summary_data:
        ret_summary[s[1]] +=s[0]
    cursor.close()
    conn.close()
    return ret_summary

def insert_user_cart_products(user_id, product_id) -> List[dict]:
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()

    query = f"insert into USERSWISHLIST(user_id, PRODUCT_ID) values({user_id},'{str(product_id)}')"
    print(query)
    cursor.execute(query)
    return 

def delete_user_cart_products(user_id, product_id) -> List[dict]:
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()

    query = f"delete from USERSWISHLIST where user_id = {user_id} and PRODUCT_ID = '{str(product_id)}'"
    print(query)
    cursor.execute(query)
    return ""