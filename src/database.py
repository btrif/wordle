#  Created by btrif Trif on 09-03-2023 , 12:14 PM.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "../data/english_words.sqlite3"
SQLITE_DATABASE = "sqlite:///"+DB_URL


db_engine = create_engine(
        SQLITE_DATABASE, connect_args={"check_same_thread" : False}
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

# Construct a base class for declarative class definitions.
#
# The new base class will be given a metaclass that produces
# appropriate :class:`~sqlalchemy.schema.Table` objects and makes
# the appropriate :class:`_orm.Mapper` calls based on the
# information provided declaratively in the class and any subclasses
# of the class.
Base = declarative_base()


# Dependency
def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()




'''             === SQLITE3 IMPLEMENTETATION FOR REGEXP     ===
You must make a method called regexp in order to use it with SQLite3

import sqlite3
import re

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

conn = sqlite3.connect('thunderbird_manufacturing.db')
conn.create_function("REGEXP", 2, regexp)
cursor = conn.cursor()

stmt="SELECT * FROM CUSTOMER WHERE ADDRESS REGEXP \'.*(Blvd|St)$\'"
cursor.execute(stmt)

print(cursor.fetchall())
'''
