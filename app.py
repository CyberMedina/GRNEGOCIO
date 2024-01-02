import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, text
from dotenv import load_dotenv
from models import *
load_dotenv()
from flask import Flask, render_template
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine= create_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True,
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
)
db = scoped_session(sessionmaker(bind=engine))




@app.route('/')
def index():
    return render_template('index.html')

 