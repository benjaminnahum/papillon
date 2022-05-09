
from pywebio import *
from pywebio.output import *
from pywebio.input import *

#!! SQLModel related code is forked from its tutorial:
# https://sqlmodel.tiangolo.com/tutorial/
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

sqlite_file_name = "sqlmodel_pywebio.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes(user_data):
    user_hero = Hero(name=user_data['name'],
        secret_name=user_data['secret_name'],
        age=user_data['age']
    )
    with Session(engine) as session:
        session.add(user_hero)
        session.commit() 
        
def main():
    put_markdown('# A Pythonic way to create a DB powered web app using `SQLModel` and `PyWebIO`')
    
    user_data = input_group("Add your own super hero",[
        input('Your Hero\'s Name (required)', name='name', required=True),
        input('Secret Name (required)', name='secret_name', required=True),
        input('Age (optional)', name='age', type=NUMBER)
    ])
    create_db_and_tables()
    create_heroes(user_data)

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)