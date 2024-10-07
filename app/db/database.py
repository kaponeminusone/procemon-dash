from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import URL


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password='1234',
    host="localhost",
    database="procemon",
    port=5432,
)

engine = create_engine(url)

meta = MetaData()
conn = engine.connect()