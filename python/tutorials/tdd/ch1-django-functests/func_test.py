
from selenium import webdriver


PORT = 8080

browser = webdriver.Firefox()
browser.get('http://localhost:{}'.format(PORT))

assert 'Django' in browser.title
