from sqlmodel import create_engine,Session,SQLModel

from config import Config

# import to load models ( creating tables programmatically )
from models.user import User
from models.cabinet import Cabinet


engine = create_engine(Config.DB_URL)

def get_session():
    with Session(engine) as session:
        yield session


def test_db_connection():
    try :
        with engine.connect() as conn:
            conn.exec_driver_sql('SELECT 1')
        print("Databse connect successfully.")
    except Exception as err:
        print("Database connection failed!")
        print("Error: ", err)
        raise SystemExit("Exiting due to DB connection failure.")


def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        print("Tables checked/created\n")
    except Exception as e:
        print("Table creation error.........! create_db_and_tables function\n",e)