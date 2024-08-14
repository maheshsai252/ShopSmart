from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os
from tasks.download_from_s3 import download_from_s3
from tasks.product.clean_product_info import clean_product_info
from tasks.product.sumarise_product_info import summarise_product_info
from tasks.product.upload_products import upload_products, upload_products_to_snowflake_function, upload_products_summaries_to_snowflake_function
from tasks.product.validate_products import validate_data_task_function, validate_product_summaries_function

from tasks.reviews.validate_reviews import validate_review_data_task_function
from tasks.reviews.clean_reviews import clean_reviews
from tasks.reviews.summarise_reviews import summarise_reviews
from tasks.reviews.upload_reviews import upload_reviews_to_snowflake_function, upload_reviews

from tasks.extract_products_and_reviews.extract_products import extract
from tasks.extract_products_and_reviews.extract_reviews import fetch_reviews

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

extract_dag = DAG(
    'Extract',
    default_args=default_args,
    description='Extract products/reviews',
    start_date=datetime(2024, 3, 19),
    schedule_interval=None,
    catchup=False
)

products_dag = DAG(
    'Products',
    default_args=default_args,
    description='Process products',
    start_date=datetime(2024, 3, 19),
    schedule_interval=None,
    catchup=False
)
reviews_dag = DAG(
    'Reviews',
    default_args=default_args,
    description='Process Reviews',
    start_date=datetime(2024, 3, 19),
    schedule_interval=None,
    catchup=False
)

def remove_files_task(**context):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    run_id = context['dag_run'].run_id
    res_path = os.path.join(res_path, str(run_id))

    for filename in os.listdir(res_path):
        file_path = os.path.join(res_path, filename)
        # Check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)
    os.rmdir(res_path)

# Products tasks 
clean_product_info_task = PythonOperator(
        task_id='clean_product_info',
        python_callable=clean_product_info,
        dag=products_dag
    )
validate_data_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data_task_function,
        dag=products_dag
    )
summarise_product_info_task = PythonOperator(
        task_id='summarise_product_info',
        python_callable=summarise_product_info,
        dag=products_dag
    )

validate_product_summaries_task = PythonOperator(
        task_id='validate_product_summaries',
        python_callable=validate_product_summaries_function,
        dag=products_dag
    )

upload_products_task = PythonOperator(
        task_id='upload_products_pinecone',
        python_callable=upload_products,
        dag=products_dag
    )
upload_products_snowflake_task = PythonOperator(
        task_id='upload_products_snowflake',
        python_callable=upload_products_to_snowflake_function,
        dag=products_dag
    )
upload_products_summaries_to_snowflake_task = PythonOperator(
        task_id='upload_products_summaries_to_snowflake_task',
        python_callable=upload_products_summaries_to_snowflake_function,
        dag=products_dag
    )
clean_reviews_task = PythonOperator(
        task_id='clean_reviews_task',
        python_callable=clean_reviews,
        dag=reviews_dag
    )
summarise_reviews_task = PythonOperator(
        task_id='summarise_reviews_task',
        python_callable=summarise_reviews,
        dag=reviews_dag
    )

upload_reviews_task = PythonOperator(
        task_id='upload_reviews_task',
        python_callable=upload_reviews,
        dag=reviews_dag
    )
validate_review_data_task =  PythonOperator(
        task_id='validate_review_data_task',
        python_callable=validate_review_data_task_function,
        dag=reviews_dag
    )
upload_reviews_to_snowflake_task = PythonOperator(
        task_id='upload_reviews_to_snowflake_task',
        python_callable=upload_reviews_to_snowflake_function,
        dag=reviews_dag
    )
extract_products =  PythonOperator(
        task_id='extract_products_from_datasource',
        python_callable=extract,
        dag=extract_dag
    )

extract_reviews =  PythonOperator(
        task_id='extract_reviews_from_datasource',
        python_callable=fetch_reviews,
        dag=extract_dag
    )


extract_products >> extract_reviews

clean_product_info_task >> validate_data_task >> upload_products_snowflake_task
clean_product_info_task >> summarise_product_info_task >> upload_products_task
summarise_product_info_task >> validate_product_summaries_task >> upload_products_summaries_to_snowflake_task

clean_reviews_task >> summarise_reviews_task >> validate_review_data_task >> upload_reviews_task
summarise_reviews_task >> upload_reviews_to_snowflake_task