import math
import re
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from alertaemail import send_mail
from funcoes import remove_duplicado


url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Configurações iniciais
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
driver = webdriver.Chrome()
# driver.implicitly_wait(60)  # seconds
driver.get(url)
# driver.maximize_window()

# Opções do site da caixa para busca de imóveis
# estado = driver.find_element(By.ID, "cmb_estado")
# select = Select(estado)
# select.select_by_value("GO")
# time.sleep(5)

estado = driver.find_element(By.NAME, "cmb_estado")
select = Select(estado)
select.select_by_visible_text("GO")


time.sleep(5)

driver.quit()
