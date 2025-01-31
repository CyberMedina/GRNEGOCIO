import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True)
db_session = scoped_session(sessionmaker(bind=engine))