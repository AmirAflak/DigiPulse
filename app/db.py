import pathlib 
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv 

# load env variables
load_dotenv()
ASTRA_CLIENT_ID = os.environ.get("ASTRA_CLIENT_ID")
ASTRA_CLIENT_SECRET = os.environ.get("ASTRA_CLIENT_SECRET")

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
    return get_cluster().connect()

session = get_session()
row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")
