from dataclasses import dataclass 
from fake_useragent import UserAgent

from .config import get_settings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup

import time 

settings = get_settings()

DRIVER_PATH = settings.driver_path

def get_user_agent():
    return UserAgent().random

@dataclass
class Scraper:
    url: str = None
    dkp: str = None 
    driver: WebDriver = None 
    endless_scroll: bool = False 
    endless_scroll_time: int = 5
    html_obj: BeautifulSoup = None
    
    def __post_init__(self):  
              
        self.url = f"https://www.digikala.com/product/{self.dkp}"
        
        if not self.dkp or not self.url:
            raise Exception(f"dkp or url is required.")
    
    def get_driver(self):
        if self.driver is None:
            user_agent = get_user_agent()
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument(f"user-agent={user_agent}")
            # driver = webdriver.Chrome(options=options)
            
            # Specify the path to your ChromeDriver executable
            chrome_driver_path = DRIVER_PATH
            
            # Update the ChromeDriver executable path and make sure it matches
            # your current Chrome browser version
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            
            self.driver = driver
        return self.driver
    
    def perform_endless_scroll(self, driver):
        if driver is not None:
            if self.endless_scroll:
                current_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(self.endless_scroll_time)
                    iter_height = driver.execute_script("return document.body.scrollHeight")
                    if current_height == iter_height:
                        break
                    current_height = iter_height
        return 
    
    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        
        if self.endless_scroll:
            self.perform_endless_scroll(driver)  
        else:
            time.sleep(10)  
         
        return driver.page_source
    
    def get_html_obj(self):
        if self.html_obj is None:
            html_str = self.get()
            self.html_obj = BeautifulSoup(html_str, "html.parser") 
        return self.html_obj
    
    def extract_element_text(self, tag, **kwargs):
        html_obj = self.get_html_obj()
        el = html_obj.find(tag, kwargs)
        if not el:
            return ''
        return el.text
    
    def _perform_price_selection(self):
        price_selectors = [
        "span.color-800.ml-1.text-h4",     # Selector for the first variation
        "span.text-h4.ml-1.color-800"      # Selector for the second variation
        ]
        
        price_str = None
        for selector in price_selectors:
            price_element = self.html_obj.select_one(selector)
            if price_element:
                price_str = price_element.text
                break
            
        # Check if the price was found
        return price_str if price_str else ''
    
        
    def perform_scrape(self):
        html_obj = self.get_html_obj()
        
        dkp = self.extract_element_text("span", **{"class": "text-caption color-400"})
        dkp = dkp.strip() if dkp is not None else None
        
        price_str = self._perform_price_selection()
        price_str = float(price_str.strip().replace(',', '')) if price_str is not None else None
        
        title_str = self.extract_element_text("h1", **{"data-testid": "PDP_TITLE"})
        title_str = title_str.strip() if title_str is not None else None
        
        return {
            "dkp": dkp,
            "price_str": price_str,
            "title": title_str
        }
            

            

            
            
            
            
        
        
        