from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Firefox()
driver.get('http://127.0.0.1:5000/test')

select = Select(driver.find_element_by_id('cars'))

# select by visible text
select.select_by_visible_text('Audi')
time.sleep(5)
