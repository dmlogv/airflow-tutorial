from datetime import datetime, timedelta
from os import getenv
from random import randint

import pyodbc

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


def test_randy():
    r = Randy()
    for _ in r:
        print(_)


prev_host, conn, cursor = None, None, None

for host, db in sorted(sql_server_ds, key=lambda x: x.conn_id):
    print(host, db)

    if not host == prev_host:
        prev_host = host
        conn = pyodbc.connect(
            server=host, database='master',
            user='sa', password=getenv('SA_PASSWORD'),
            autocommit=True)

        cursor = conn.cursor()

    print('Create DB', db)
    cursor.execute('CREATE DATABASE %s', db)

    print('Create table')
    cursor.execute("""
        USE %s;
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
    conn.commit()

    print('Done')
