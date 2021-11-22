import os
import pymysql
import datetime

from sqlalchemy.sql.expression import true

DB_HOST = "localhost"#os.getenv("DB_HOST")
DB_USER = "root" #os.getenv("DB_USER")
DB_PASS = "" #os.getenv("DB_PASS")
DB_NAME = "skoly" #os.getenv("DB_NAME")

DEBUG = true

SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
DATABASE_CONNECT_OPTIONS = {}