from datetime import datetime, timedelta
from os import getenv
from random import randint
from sys import stderr
from time import sleep
from concurrent.futures import ThreadPoolExecutor

import pymssql

from commons.datasources import sql_server_ds


class Randy:
    def __init__(self):
        self.seed = randint(1575e6, 1590e6)
        self.start = datetime.utcfromtimestamp(self.seed)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        shift = timedelta(seconds=randint(10, 100)) * self.i
        interval = timedelta(seconds=randint(100, 1000))
        self.i += 1
        return (self.start + shift,
                self.start + shift + interval,
                randint(-100, 100))


print('Wait...')
sleep(30)


def init_db(host, db):
    print(host, db)

    with pymssql.connect(
        server=host, database='master',
        user='sa', password=getenv('SA_PASSWORD')) as conn:

        with conn.cursor() as cursor:
            print('Create DB', db)
            conn.autocommit(True)
            cursor.execute(f'CREATE DATABASE {db}')

            print('Create table')
            cursor.execute(f"""
                USE {db};
                CREATE TABLE dbo.Orders (
                    id         bigint IDENTITY(1, 1) PRIMARY KEY,
                    start_time datetime2, 
                    end_time   datetime2, 
                    type       int,
                    data       uniqueidentifier DEFAULT NEWID()
                )
                """)

            print('Put data')
            r = Randy()
            conn.autocommit(False)
            cursor.executemany("""
                INSERT dbo.Orders(start_time, end_time, type)
                VALUES (%s, %s, %s)
                """, [next(r) for _ in range(randint(1000, 2000))])

            print('Check')
            cursor.execute('SELECT COUNT(1) FROM dbo.Orders')
            print('Inserted', cursor.fetchone()[0])
            conn.commit()

            print('Done')


def suppress_exceptions(f, *args, **kwargs):
    retries = 5
    for i in range(retries):
        try:
            f(*args, **kwargs)
        except Exception as e:
            print(f.__name__, *args, *kwargs, e,
                  'Try', i, '/', retries, file=stderr)
            sleep(randint(5, 20))
        else:
            break


pool = ThreadPoolExecutor(max_workers=20)
for host, db in sorted(sql_server_ds, key=lambda x: x.conn_id):
    pool.submit(suppress_exceptions, init_db, host, db)

