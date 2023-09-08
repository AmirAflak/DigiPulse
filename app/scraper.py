from dataclasses import dataclass 
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service

import time


def get_user_agent():
    return UserAgent().random

@dataclass
class Scraper:
    url: str 
    driver: WebDriver = None 
    endless_scroll: bool = False 
    endless_scroll_time: int = 5
    
    def get_driver(self):
        if self.driver is None:
            user_agent = get_user_agent()
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument(f"user-agent={user_agent}")
            # driver = webdriver.Chrome(options=options)
            
            # Specify the path to your ChromeDriver executable
            chrome_driver_path = '/home/mehrdad/chromedriver-linux64/chromedriver'
            
            # Update the ChromeDriver executable path and make sure it matches
            # your current Chrome browser version
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            
            self.driver = driver
        return self.driver
    
    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        
        if self.endless_scroll:
            current_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, documnet.body.scrollHeight)")
                time.sleep(self.endless_scroll_time)
                iter_height = driver.execute_script("return document.body.scrollHeight")
                if current_height == iter_height:
                    break
                current_height = iter_height
                
        return driver.page_source
                
    