import pendulum
import subprocess
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def full_update():
    subprocess.run(
        ["python", "/opt/project/fpl.py", "-u"],
        check=True
    )

with DAG(
    dag_id='full_update',
    schedule=timedelta(minutes=15),
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=['full_update'],
) as dag:
    task = PythonOperator(
        task_id='full_update_task',
        python_callable=full_update
    )
