
from selenium import webdriver
import logging


PORT = 8000


logging.basicConfig(
    level=logging.INFO
)


browser = webdriver.Firefox()
browser.get('http://localhost:{}'.format(PORT))

assert 'Django' in browser.title
logging.info("Tests passed successfully...")
