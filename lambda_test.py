import sqlalchemy as db
import json
import sys
import psycopg2
from sqlalchemy.dialects.postgresql import insert


engine = db.create_engine('postgresql://openview:postgres_free@database-ecb.cxkslz20bb7r.eu-central-1.rds.amazonaws.com:5432/postgres')


connection = engine.connect()

metadata = db.MetaData()


exchange = db.Table('exchange_rates',metadata, autoload=True, autoload_with=engine)



print(engine.execute("SELECT * from exchange_rates where name = 'JPY'").fetchall())
