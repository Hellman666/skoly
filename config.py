import os
import pymysql
import datetime

DB_HOST = "localhost"#os.getenv("DB_HOST")
DB_USER = "root" #os.getenv("DB_USER")
DB_PASS = "" #os.getenv("DB_PASS")
DB_NAME = "skoly" #os.getenv("DB_NAME")

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
DATABASE_CONNECT_OPTIONS = {}