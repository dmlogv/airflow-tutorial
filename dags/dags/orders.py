import csv
from datetime import timedelta, datetime
from io import StringIO

import pandas as pd
from airflow import DAG
from airflow.contrib.hooks.vertica_hook import VerticaHook
from airflow.contrib.operators.vertica_operator import VerticaOperator
from airflow.hooks.mssql_hook import MsSqlHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from pandas.util import hash_pandas_object

from commons.datasources import sql_server_ds
from commons.session import Session


dag = DAG('orders',
          schedule_interval=timedelta(hours=6),
          start_date=datetime(2020, 2, 8, 0),
          default_args={'retries': 3, 'retry_delay': timedelta(seconds=10)},
          catchup=True)

target_conn_id = 'dwh'
target_schema = 'stage'
target_table = 'Orders'


def workflow(src_conn_id, src_schema, dt,
             target_conn_id, target_table):
    # TODO Split code into functions
    etl_conn = PostgresHook(postgres_conn_id='etl').get_conn()

    with Session(etl_conn, f'{dag.dag_id}__{src_schema}') as session:
        # Load data
        source_conn = MsSqlHook(mssql_conn_id=src_conn_id, schema=src_schema).get_conn()

        query = """
            SELECT 
                id, start_time, end_time, type, data
            FROM dbo.Orders
            WHERE
                CONVERT(DATE, start_time) = %s
            """

        df = pd.read_sql_query(query, source_conn, params=(dt,))

        # Add service fields
        df['etl_source'] = src_schema
        df['etl_id'] = session.id
        df['hash_id'] = hash_pandas_object(df[['etl_source', 'id']])

        # Export data to CSV buffer
        buffer = StringIO()
        df.to_csv(buffer,
                  index=False, sep='|', na_rep='NUL', quoting=csv.QUOTE_MINIMAL,
                  header=False, float_format='%.8f', doublequote=False, escapechar='\\')
        buffer.seek(0)

        # Push CSV
        target_conn = VerticaHook(vertica_conn_id=target_conn_id).get_conn()

        copy_stmt = f"""
            COPY {target_table}({df.columns.to_list()}) 
            FROM STDIN 
            DELIMITER '|' 
            ENCLOSED '"' 
            ABORT ON ERROR 
            NULL 'NUL'
            """

        cursor = target_conn.cursor()
        cursor.copy(copy_stmt, buffer)

        session.loaded_rows = cursor.rowcount
        session.successful = True


create_schema_query = f'CREATE SCHEMA IF NOT EXISTS {target_schema};'
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {target_schema}.{target_table} (
         id         INT,
         start_time TIMESTAMP,
         end_time   TIMESTAMP,
         type       INT,
         data       VARCHAR(32),
         etl_source VARCHAR(200),
         etl_id     INT,
         hash_id    INT PRIMARY KEY
     );"""

create_table = VerticaOperator(
    task_id='create_target',
    sql=[create_schema_query,
         create_table_query],
    vertica_conn_id=target_conn_id,
    task_concurrency=1,
    dag=dag)


for conn_id, schema in sql_server_ds:
    load = PythonOperator(
        task_id=schema,
        python_callable=workflow,
        op_kwargs={
            'src_conn_id': conn_id,
            'src_schema': schema,
            'dt': '{{ ds }}',
            'target_conn_id': target_conn_id,
            'target_table': f'{target_schema}.{target_table}'},
        dag=dag)

    create_table >> load
