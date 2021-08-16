from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from flask_jwt_extended import JWTManager
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@127.0.0.1/company_base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE = declarative_base()
ENGINE = create_engine('postgresql://root:root@127.0.0.1/company_base', echo=False)
Session = sessionmaker(bind=ENGINE)
SESSION = orm.scoped_session(Session)
jwt = JWTManager(app)
jwt_secret_key = '7t4bauR5P8gP5dHEgWbtIstS18bmNIea'