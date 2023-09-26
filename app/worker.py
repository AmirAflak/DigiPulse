from celery import Celery
from celery.signals import beat_init, worker_process_init
from celery.schedules import crontab
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from .models import Product, ProductScrapeEvent
from .config import get_settings
from .db import get_cluster
from .scraper import Scraper
from .schema import ProductSchema
from .crud import add_scrape_event


celery_app = Celery(__name__)
settings = get_settings()
first_time = True
PRODUCTS_PAGE_URL = settings.products_page_url

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
    sync_table(Product)
    sync_table(ProductScrapeEvent)
    
worker_process_init.connect(celery_on_startup)
beat_init.connect(celery_on_startup)


@celery_app.on_after_configure.connect 
def setup_periodic_task(sender, *args, **kwargs):
    sender.add_periodic_task(crontab(minute="*/15"),
                             scrape_products.s(products_page_url))

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
def scrape_products(url):
    global first_time
    if first_time:
        dkp_list = Scraper(url=url, fetch_products=True).perform_scrape()
        first_time = False
    else:
        dkp_list = list(Product.objects().all().values_list("dkp", flat=True))
        
    for dkp in dkp_list:
        scrape_dkp.delay(dkp)