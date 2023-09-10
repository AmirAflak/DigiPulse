from app import db, worker, models
from bs4 import BeautifulSoup

def test_scrape_dkp():
    # Set up
    session = db.get_session()
    dkp = 'dkp-11153044'
    url = "https://www.digikala.com/product/dkp-11153044"
    
    # Execute the function under test
    result = worker.scrape_dkp(dkp)
    
    # Assert the expected results
    assert isinstance(result, models.Product)
    
