from celery import Celery
from celery.signals import beat_init, worker_process_init
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from .models import Product, ProductScrapeEvent
from .config import get_settings
from .db import get_cluster, get_session


celery_app = Celery(__name__)
settings = get_settings()

REDIS_URL = settings.redis_url
celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL

def celery_on_startup(*args, **kwargs):
    if connection.cluster is not None:
        connection.cluster.shutdown()
    if connection.session is not None:
        connection.session.shutdown()
    cluster = get_cluster()
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    # get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)
    
beat_init.connect(celery_on_startup)
worker_process_init.connect(celery_on_startup)

@celery_app.on_after_configure.connect 
def setup_periodic_task(sender, *args, **kwargs):
    sender.add_periodic_task(1, random_task.s("random_task Helloo !!"))

@celery_app.task
def random_task(name):
    print(f"Hello from {name}")
    
@celery_app.task 
def list_products():
    print(list(Product.objects().all().values_list("dkp", flat=True)))