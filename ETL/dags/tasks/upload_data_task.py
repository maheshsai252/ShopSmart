from helpers.upload_to_snowflake_helper import upload_data_to_snowflake, upload_metadata_to_snowflake

def upload_data_to_snowflake_task(**context):
    print(context)
    if 'task_instance' in context:
        task_instance = context['task_instance']
        run_id = context['dag_run'].run_id
        data = task_instance.xcom_pull(task_ids='validate_data')
        print("Ds", data)
        upload_data_to_snowflake(run_id,csv_filename=data)
    else:
        return "error"
    return "completed"
def upload_metadata_data_to_snowflake_task(**context):
    print(context)
    if 'task_instance' in context:
        task_instance = context['task_instance']
        run_id = context['dag_run'].run_id
        data = task_instance.xcom_pull(task_ids='validate_meta_data')
        print("Ds", data)
        upload_metadata_to_snowflake(run_id,csv_filename=data)
    else:
        return "error"
    return "completed"