from celery import Celery
from celery.signals import beat_init, worker_process_init
from celery.schedules import crontab
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from .models import Product, ProductScrapeEvent
from .config import get_settings
from .db import get_cluster, get_session
from .scraper import Scraper
from .schema import ProductSchema
from .crud import add_scrape_event

import threading

# thread_local = threading.local()



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
    # thread_local.cassandra_session = session
    sync_table(Product)
    sync_table(ProductScrapeEvent)
    
worker_process_init.connect(celery_on_startup)
beat_init.connect(celery_on_startup)


@celery_app.on_after_configure.connect 
def setup_periodic_task(sender, *args, **kwargs):
    # sender.add_periodic_task(1, random_task.s("random_task Helloo !!"), expires=10)
    # sender.add_periodic_task(crontab(hour=8, minute=0, day_of_week=2),
    #                          random_task.s("random_task Helloo !!"), expires=10)
    sender.add_periodic_task(crontab(minute="*/5"),
                             scrape_products.s())

@celery_app.task
def random_task(name):
    print(f"Hello from {name}")
    
@celery_app.task 
def list_products():
    print(list(Product.objects().all().values_list("dkp", flat=True)))
    
@celery_app.task
def scrape_dkp(dkp):
    data = Scraper(dkp=dkp, endless_scroll=True).perform_scrape()
    try:
        validated_data = ProductSchema(**data)
    except:
        validated_data = None
    if validated_data is not None:
        product, _ = add_scrape_event(validated_data.dict())
        return product
    
@celery_app.task
def scrape_products():
    print("Doing Scraping Job...")
    # q = list(Product.objects().all().values_list("dkp", flat=True))
    q = ['dkp-2271206', 'dkp-749878', 'dkp-11153044']
    for dkp in q:
        scrape_dkp.delay(dkp)