from helpers.validate_with_pydantic_helper import validate_data, validate_product_summaries

def validate_data_task_function(**context):
    task_instance = context['task_instance']
    # run_id = context['dag_run'].run_id
    data = task_instance.xcom_pull(task_ids='clean_product_info')    
    return validate_data(data)

def validate_product_summaries_function(**context):
    task_instance = context['task_instance']
    # run_id = context['dag_run'].run_id
    data = task_instance.xcom_pull(task_ids='summarise_product_info')    
    return validate_product_summaries(data)
