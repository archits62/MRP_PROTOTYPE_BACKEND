from sqlmodel import create_engine,Session

from config import Config


engine = create_engine(Config.DB_URL,echo=True)

def get_session():
    with Session(engine) as session:
        yield session


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

def test_db_connection():
    try :
        with engine.connect() as conn:
            conn.exec_driver_sql('SELECT 1')
        print("Databse connect successfully.")
    except Exception as err:
        print("Database connection failed!")
        print("Error: ", err)
        raise SystemExit("Exiting due to DB connection failure.")

