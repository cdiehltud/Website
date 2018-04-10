import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config)

#db= SQLAlchemy(app)

#from app.views import user
from app.views import pflegedienst



#app.config['DEBUG'] = config.DEBUG
#app.config['SECRET_KEY']= os.urandom(24)
#app.config['STRIPE_API_KEY']= config.STRIPE_API_KEY
#app.config['SQLALCHEMY_DATABASE_URI']= config.SQLALCHEMY_DATABASE_URI
#app.config['SQLALCHEMY_ECHO']= config.SQLALCHEMY_ECHO
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= config.SQLALCHEMY_TRACK_MODIFICATIONS