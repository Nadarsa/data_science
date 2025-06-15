import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Путь к корню проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Директории для логов и скриптов
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Общие настройки DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
    "execution_timeout": timedelta(minutes=20),
    "start_date": datetime(2025, 6, 10),
}

with DAG(
    dag_id="ml_pipeline_bash_operator",
    description="ML pipeline for breast cancer using BashOperator",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["ml", "bash", "pipeline"],
) as dag:

    # ЗАДАЧА 1 — загрузка данных
    load_task = BashOperator(
        task_id="load_data",
        bash_command=(
            f"PYTHONPATH={PROJECT_ROOT} "
            f"python -m etl.load_data "
            f" >> {os.path.join(LOG_DIR, 'load_data.log')} 2>&1"
        )
    )

    # ЗАДАЧА 2 — предобработка
    preprocess_task = BashOperator(
        task_id="preprocess_data",
        bash_command=(
            f"PYTHONPATH={PROJECT_ROOT} "
            f"python -m etl.preprocess "
            f" >> {os.path.join(LOG_DIR, 'preprocess_data.log')} 2>&1"
        )
    )

    # ЗАДАЧА 3 — обучение модели
    train_task = BashOperator(
        task_id="train_model",
        bash_command=(
            f"PYTHONPATH={PROJECT_ROOT} "
            f"python -m etl.train_model "
            f" >> {os.path.join(LOG_DIR, 'train_model.log')} 2>&1"
        )
    )

    # ЗАДАЧА 4 — оценка модели
    evaluate_task = BashOperator(
        task_id="evaluate_model",
        bash_command=(
            f"PYTHONPATH={PROJECT_ROOT} "
            f"python -m etl.evaluate "
            f" >> {os.path.join(LOG_DIR, 'evaluate_model.log')} 2>&1"
        )
    )

    # Зависимости: поэтапная последовательность
    load_task >> preprocess_task >> train_task >> evaluate_task
