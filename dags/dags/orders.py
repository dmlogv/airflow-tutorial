from collections import defaultdict
from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from commons.datasources import sql_server_ds

default_args = {
    'start_date': datetime(2020, 7, 8, 0)
    }

dag = DAG('orders', schedule_interval=timedelta(hours=6),
          default_args=default_args)


def workflow(**context):
    print(context)


groups = {}

for conn_id, schema in sql_server_ds:
    group = groups.setdefault(conn_id, DummyOperator(
        task_id=conn_id, dag=dag))

    load = PythonOperator(
        task_id=schema,
        python_callable=workflow,
        provide_context=True,
        dag=dag)

    group >> load
