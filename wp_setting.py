from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("")