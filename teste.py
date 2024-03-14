from selenium import webdriver
import time


# Configurações iniciais
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

time.sleep(2)

driver.get("https://www.selenium.dev/selenium/web/web-form.html")
# driver.maximize_window()
time.sleep(2)
driver.quit()
