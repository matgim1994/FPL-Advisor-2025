import json
import pendulum
from datetime import datetime, timedelta
from airflow.sdk import dag, task


@dag(
    schedule=timedelta(minutes=1),
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=['test'],
)
def test_dag():
    @task()
    def print_hello():
        config = {
            "env": "{{ var.value.FPL_ENV }}",
            "message": "Hello, Airflow!"
        }
        print(json.dumps(config, indent=2))

    print_hello()


test_dag()
