import selenium
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from enum import Enum
import time

class Selectors(Enum):
    CSS_SELECTOR = By.CSS_SELECTOR
    CLASS_NAME = By.CLASS_NAME
    NAME = By.NAME
    ID = By.ID
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    TAG_NAME = By.TAG_NAME

class Scraper:

    def __init__(self, waittime: int, headless: bool):

        service = Service(executable_path="Python/Scraping/chromedriver.exe")

        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        if headless: options.add_argument("--headless=new")

        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

        self.driver = uc.Chrome(service=service,options=options)
        self.waittime = waittime

    def get(self, url: str):
        self.driver.get(url)

    def wait(self, selector, id):
        WebDriverWait(self.driver, self.waittime).until(EC.presence_of_element_located((selector, id)))

    def waitforall(self, selector, id):
        WebDriverWait(self.driver, self.waittime).until(EC.presence_of_all_elements_located((selector, id)))

    def quit(self):
        self.driver.quit()

    def find(self, selector: Selectors, id: str):
        try:
            self.wait(selector.value, id)
            return self.driver.find_element(selector.value, id)
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException):
            return False
    
    def find_all(self, selector: Selectors, id: str):
        try:
            self.wait(selector.value, id)
            return self.driver.find_elements(selector.value, id)
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException):
            return False
    
    def find_in(self, element, selector: Selectors, id: str):
        try:
            # self.wait(selector.value, id)
            return element.find_element(selector.value, id)
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException):
            return False
        
    def find_in_all(self, element, selector: Selectors, id: str):
        try:
            # self.wait(selector.value, id)
            return element.find_elements(selector.value, id)
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException):
            return False
        
    def click(self, element):
        WebDriverWait(self.driver, self.waittime).until(EC.element_to_be_clickable(element))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()
