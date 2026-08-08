from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_link():
	# set up the browser driver
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	# navigate to a page
	driver.get("http://127.0.0.1:5000/")
 
	link = driver.find_element(By.TAG_NAME, "h1")
	
	assert link.text == "Items"

	input_box = driver.find_element(By.ID, "item-name")
	input_box.send_keys("Bananas")

	button = driver.find_element(By.ID, "add-button")
	button.click()
	
	item_list = driver.find_element(By.ID, "item-list")
	wait = WebDriverWait(driver, 10)
	wait.until(EC.text_to_be_present_in_element((By.ID, "item-list"), "Bananas"))
	time.sleep(0.5)
	assert "Bananas" in item_list.text

	# close the browser
	driver.quit()