from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from app.db.database import engine, meta #TODO: add Barrel

users = Table("users", meta, 
              Column("id", Integer, primary_key=True), 
              Column("name", String(255)),
              Column("email", String(255))
              )

meta.create_all(engine)