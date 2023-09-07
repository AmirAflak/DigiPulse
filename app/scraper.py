from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service


def get_user_agent():
    return UserAgent().random

class Scraper:
    driver: WebDriver = None 
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
    