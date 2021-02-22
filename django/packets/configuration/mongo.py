import os

MONGO_DB = ""
MONGO_USER = ""
MONGO_PASSWORD = ""
MONGO_HOST = ""
MONGO_PORT = ""
MONGO_AUTH_SOURCE = ""
MONGO_COLLECTION = ""

if "MONGO_DB" in os.environ:
    MONGO_DB = os.environ['MONGO_DB']
if "MONGO_USER" in os.environ:
    MONGO_USER = os.environ['MONGO_USER']
if "MONGO_PASSWORD" in os.environ:
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
if "MONGO_HOST" in os.environ:
    MONGO_HOST = os.environ['MONGO_HOST']
if "MONGO_PORT" in os.environ:
    MONGO_PORT = os.environ['MONGO_PORT']
if "MONGO_AUTH_SOURCE" in os.environ:
    MONGO_AUTH_SOURCE = os.environ['MONGO_AUTH_SOURCE']
if "MONGO_COLLECTION" in os.environ:
    MONGO_COLLECTION = os.environ['MONGO_COLLECTION']

