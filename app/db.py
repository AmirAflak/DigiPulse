import pathlib 
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection
from .config import get_settings

# load settings
settings = get_settings()

ASTRA_CLIENT_ID = settings.db_client_id
ASTRA_CLIENT_SECRET = settings.db_client_secret

# app/
BASE_DIR = pathlib.Path(__file__).parent 
# bundle path
CLUSTER_BUNDLE = str(BASE_DIR / "ignored" / "secure-connect-fastapi-df.zip")


def get_cluster():
    cloud_config= {
    'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
    return Cluster(cloud=cloud_config, auth_provider=auth_provider)

def get_session():
    session = get_cluster().connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session

