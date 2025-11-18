import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import get_driver
import time

class Task_Page():
    def __init__(self):
        self.driver = get_driver()

    
    def open(self):
        self.driver.get(config.BASE_URL)
    

    def type(self, text:str):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        element = self.driver.find_element(By.NAME,"title")
        print(element.text)
        element.clear()
        element.send_keys(text, Keys.ENTER)
        time.sleep(config.IMPLICIT_WAIT)
    
    def get_to_do_list_all(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        element = self.driver.find_element(By.LINK_TEXT, "All")
        element.click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "toggle"))
        )
        elements = self.driver.find_elements(By.CLASS_NAME, "toggle")
        print(len(elements))
        time.sleep(config.IMPLICIT_WAIT)
    

    def get_todos(driver):
        """Return list of <li> todo elements."""
        return driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li")


    def stop(self):
        self.driver.quit()
        


    

