from helpers.validate_with_pydantic_helper import validate_review_summaries


def validate_review_data_task_function(**context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='summarise_reviews_task')    
    return validate_review_summaries(data)