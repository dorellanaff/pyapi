from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile, Chrome
from selenium.webdriver.common.keys import Keys
# Selenium Explicit Waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime,sleep
import datetime

url = 'http://certificados.ministeriodegobierno.gob.ec/gestorcertificados/antecedentes/'

class selenium:
    ff = FirefoxOptions()
    ff.headless = True # Cambiar a False, para ejecutar Firefox en modo ventana

    def __init__(self):
        self.driver = Firefox(options=self.ff, executable_path='geckodriver')
        print('Iniciado')
        pass

    def button_click(self, button, driver):
        while True:
            try:
                btn = driver.find_element_by_xpath(button)
                btn.click()
                break
            except:
                pass

    def pass_text(self, text, tagid, driver):
        while True:
            try:
                motivo = driver.find_element_by_xpath('//*[@id="{}"]'.format(tagid))
                motivo.send_keys(text)
                break
            except:
                pass

    def run(self, ci):
        re = {}
        try:
            self.driver.get(url)
            startscript = datetime.datetime.now()
            #print(driver.title)
            self.button_click('/html/body/div[5]/div[11]/button[2]/span', self.driver) # Warning button
            self.pass_text(ci, 'txtCi', self.driver)
            self.button_click('//*[@id="btnSig1"]', self.driver) # Search button
            self.pass_text('Consulta antecedentes', 'txtMotivo', self.driver)
            self.button_click('//*[@id="btnSig2"]', self.driver) # Motivo button
            #driver.implicitly_wait(2) # seconds
            name = self.driver.find_element_by_id('dvName1')
            antecedentes = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "dvAntecedent1"))) # presence_of_element_located
            print('Nombre: {}'.format(str(name.text)))
            print('Antecedentes: {}'.format(str(antecedentes.text)))
            endscript = datetime.datetime.now()
            duration = endscript - startscript
            print("Duracion script: {}".format(duration))
            re = {'CI': ci,'Name': str(name.text), 'Antecedentes': str(antecedentes.text), 'response': '{}'.format(str(duration))}
            return re
        except Exception as e:
            print(e)
            return {error}
