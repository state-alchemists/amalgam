from sqlmodel import create_engine

from myapp.config import APP_DB_URL

connect_args = {"check_same_thread": False}
db_engine = create_engine(APP_DB_URL, connect_args=connect_args, echo=True)
