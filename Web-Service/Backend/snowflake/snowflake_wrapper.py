from typing import List
import snowflake.connector
import os

snowflake_config = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': 'Marketplace',
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}
def get_product_data(products) -> List[dict]:
    conn = snowflake.connector.connect(**snowflake_config)
    asins = [product['asin'] for product in products if product.get('asin')]
    asins_str = ', '.join([f"'{asin}'" for asin in asins])
    data=[]
    summary_data = []
    try:
        cursor = conn.cursor()
        if asins:
            query = f"SELECT title, features, description, imageURLHighRes,category, asin FROM Products WHERE asin IN ({asins_str})"
            print(query)
            cursor.execute(query)
            # cursor.execute(f"SELECT title,features,description,imageURLHighRes FROM Products WHERE asin in '%{asins}%'")
        data = cursor.fetchall()
        if asins:
            query = f"SELECT summary,asin FROM ProductsSummaries WHERE asin IN {tuple(asins)}"
            cursor.execute(query)
            # cursor.execute(f"SELECT title,features,description,imageURLHighRes FROM Products WHERE asin in '%{asins}%'")
        summary_data = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
    asin_data = {row[-1]: row[:-1] for row in data}
    summaries = {row[-1]: row[:-1] for row in summary_data}

    # Update the products list with the fetched data
    for product in products:
        asin = product['asin']
        if asin in asin_data:
            title, features, description, imageURLHighRes, category = asin_data[asin]
            product.update({
                'title': title,
                'imageURLHighRes': imageURLHighRes,
                'category': category,
                'summary': summaries[asin][0] if asin in summaries and len(summaries[asin])>0 else ""
            })
        else:
            product.update({
                'title': "title",
                'imageURLHighRes': "",
                'category': "",
                'summary': ""
            })

    return products

def insert_user_searches(user_id, searches) -> List[dict]:
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        for search in searches:
            cursor.execute("INSERT INTO usersearches (user_id, search) VALUES (%s, %s)", (user_id, search))
        cursor.close()
        conn.close()
    except Exception as e:
         print(str(e))
    return "success"
def retrieve_last_5_user_searches(user_id: int) -> List[str]:
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        cursor.execute("SELECT search FROM usersearches WHERE user_id = %s ORDER BY ROW_NUMBER() OVER (ORDER BY search DESC) LIMIT 5", (user_id,))
        searches = cursor.fetchall()
        cursor.close()
        conn.close()
        search_results = [search[0] for search in searches]
        return search_results
        
    except Exception as e:
         print(str(e))
    return []

def retrieve_user_activities(user_id: int) -> List[str]:
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        cursor.execute("SELECT activity FROM usersactivities WHERE user_id = %s", (user_id,))
        activities = cursor.fetchall()
        cursor.close()
        conn.close()
        activity_results = [activity[0] for activity in activities]
        return activity_results
        
    except Exception as e:
         print(str(e))
    return []


def retrieve_user_gender(user_id: int) -> List[str]:
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        query = f"SELECT gender FROM users WHERE id = {user_id}"
        print(query, "imp")
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users[0][0].lower() if len(users) >0 else "men"
    except Exception as e:
         print(str(e))
    return "men"