import pendulum
import subprocess
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def update_raw():
    subprocess.run(['python', '/opt/project/fpl.py', '-ur'], check=True)


def run_dbt():
    subprocess.run(['python', '/opt/project/fpl.py', '-rd'], check=True)


with DAG(
    dag_id='full_update',
    schedule=timedelta(minutes=15),
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=['full_update'],
) as dag:

    t_update_raw = PythonOperator(task_id='update_raw', python_callable=update_raw)
    t_run_dbt = PythonOperator(task_id='run_dbt', python_callable=run_dbt)

    t_update_raw >> t_run_dbt
