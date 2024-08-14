# Function to get user activities from Snowflake
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

def get_user_activities(user_id):
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT ACTIVITY FROM USERSACTIVITIES WHERE USER_ID = {user_id}")
        activities = cursor.fetchall()
        return [row[0] for row in activities]
    finally:
        cursor.close()
        conn.close()