#config.py

import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import urllib.parse
import pyodbc

database = 'COMP2001_EClayton'
username = 'EClayton'
password = 'CmoZ392+'
encoded_password = urllib.parse.quote_plus(password)


basedir = pathlib.Path(__file__).parent.resolve()

connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app


app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mssql+pyodbc://{username}:{encoded_password}@DIST-6-505.uopnet.plymouth.ac.uk/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
    "&Encrypt=yes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy()
ma = Marshmallow()
db.init_app(app)
ma.init_app(app)



conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DIST-6-505.uopnet.plymouth.ac.uk;"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
    "Connection Timeout=30;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()



