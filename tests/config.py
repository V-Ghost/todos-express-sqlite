from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service()  # auto-detect ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

BASE_URL = "http://localhost:3000/"
BROWSER = "chrome"  # in future you can extend to "firefox", etc.
IMPLICIT_WAIT = 5