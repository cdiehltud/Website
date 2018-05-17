import os

STRIPE_API_KEY = 'SmFjb2IgS2FwbGFuLU1vc3MgaXMgYSBoZXJv'
DEBUG = True
SECRET_KEY= os.urandom(24)
COUCHDB_USER = os.environ.get('EA_COUCHDB_USER')
COUCHDB_PASSWORD = os.environ.get('EA_COUCHDB_PASSWORD')
COUCHDB_URL=os.environ.get("EA_COUCHDB_URL", default="http://127.0.0.1:5984/")
COUCHDB_NAME = os.environ.get('EA_COUCHDB_NAME')
