import time
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(1024, 768))
display.start()
path = './app/drivers/chromedriver'
browser = webdriver.Chrome(executable_path=path)
actions = webdriver.ActionChains(browser)
browser.get('http://certificados.ministeriodegobierno.gob.ec/gestorcertificados/antecedentes/certificado.php?idr=16489626')
print(browser.current_url)