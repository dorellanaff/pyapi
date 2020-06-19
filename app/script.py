
from selenium.webdriver.common.keys import Keys
# Selenium Explicit Waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile, Chrome
from time import strftime,sleep
import datetime, os, requests
from pyvirtualdisplay import Display

urlantecedentes = 'http://certificados.ministeriodegobierno.gob.ec/gestorcertificados/antecedentes/'
urlant = 'https://sistemaunico.ant.gob.ec:5038/PortalWEB/paginas/clientes/clp_criterio_consulta.jsp'
urlluzgye = 'http://190.120.76.177:8080/consultaplanillas/servlet/gob.ec.sapconsultas/'
urlcnt = 'https://pagarmisfacturas.cnt.gob.ec/cntpagos/php/index.php'

class selenium:
    wait = True
    download_dir = ''
    
    def __init__(self):
        self.driver = self.iniciar()
        print('Iniciado Webdriver')
        pass

    def iniciar(self): # Inicializar Webdriver
        try:
            gc = Options()
            gc.add_argument('user-data-dir=sel')
            if os.name == 'nt':
                print('Operative System> Windows')
                path = './app/drivers/chromedriver.exe' 
                self.download_dir = 'C:\\Users\\danie\\Documents\\Proyectos\\vscode\\py\\selenium\\pyantecedentes\\app\\pdf'
            else:
                print('Operative System> Unix')
                display = Display(visible=0, size=(1024, 768))
                display.start()
                #gc.add_argument('headless')
                #gc.add_argument('no-sandbox')
                path = './app/drivers/chromedriver'
                self.download_dir = '/home/daniel/py/pyantecedentes/app/pdf'  # for linux/*nix, download_dir="/usr/Public"   
            gc.add_experimental_option('prefs', {
            "download.default_directory": self.download_dir, #Change default directory for downloads
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": False,
            "plugins.always_open_pdf_externally": False #It will not show PDF directly in chrome
            })
            return Chrome(options=gc, executable_path=path)
        except Exception as e:
            print(e)

    def select_input(self, xpath, text, timeout):
        #print(xpath)
        try:
            select = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))) # presence_of_element_located
            for option in select.find_elements_by_tag_name('option'):
                if text != '':
                    if option.text in text:
                        option.click()
                else:
                    option.click()
            return True
        except Exception as e:
            return False

    def button_click(self, xpath, timeout): # Buscar boton
        #print(xpath)
        try:
            #btn = driver.find_element_by_xpath(xpath)
            btn = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))) # presence_of_element_located
            btn.click()
            return True
        except:
            return False

    def pass_text(self, text, tagid, timeout, by): # Pasar texto a elementos
        #print(tagid)
        try:
            #input = self.driver.find_element_by_xpath('//*[@id="{}"]'.format(tagid))
            if by == 1:
                input = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, tagid))) # presence_of_element_located
            else:
                input = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, tagid))) # presence_of_element_located
            input.send_keys(text)
            return True
        except:
            return False

    def check_element(self, xpath, timeout): # Buscar elemento en DOM
        #print(xpath)
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))) # presence_of_element_located
            return True
        except:
            return False

    def get_text(self, xpath, timeout): # Buscar elemento en DOM
        #print(xpath)
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))) # presence_of_element_located
            return element.text
        except:
            return ''

    def get_value(self, xpath, timeout): # Buscar elemento en DOM
        #print(xpath)
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))) # presence_of_element_located
            return element.get_attribute("value")
        except:
            return ''

    def antecedentes(self, ci): # Main
        re = []
        pdfurl = ''
        out_pdf = ''
        try:
            self.wait = False
            self.driver.get(urlantecedentes)
            self.button_click('/html/body/div[5]/div[11]/button[2]/span', 5) # Warning button
            self.pass_text(ci, 'txtCi', 5, 1)
            self.button_click('//*[@id="btnSig1"]', 5) # Search button
            if self.pass_text('Consulta antecedentes', 'txtMotivo', 15, 1):
                self.button_click('//*[@id="btnSig2"]', 5) # Motivo button
                self.button_click('//*[@id="btnOpen"]/span', 5)
                self.driver.switch_to.window(self.driver.window_handles[1])
                pdfurl = self.driver.current_url
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                out_pdf = '{}/{}.pdf'.format(self.download_dir, ci)
                if os.name == 'nt':
                    out_pdf = '{}\\{}.pdf'.format(self.download_dir, ci)
                else:
                    out_pdf = '{}/{}.pdf'.format(self.download_dir, ci)
                r = requests.get(pdfurl, stream=True, headers={'User-agent': 'Mozilla/5.0'})
                open(out_pdf , 'wb').write(r.content)
                re = True
            else:
                re = False
        except Exception as e:
            print(e)
            re = False
        finally:
            self.wait = True
            return [re, pdfurl, out_pdf]
   
    def ant(self, id): # Main
        re = []
        response = {}
        status = 404
        try:
            self.wait = False
            self.driver.get(urlant)
            self.select_input('//*[@id="ps_tipo_identificacion"]', 'PLACA', 5) # Select option
            self.pass_text(id, '//*[@id="ps_identificacion"]', 5, 0) # Input button 0. search by path
            self.button_click('//*[@id="frm_consulta"]/div/a/img', 5) # Search button
            if self.check_element('/html/body/table[1]/tbody/tr[1]/td[1]/strong', 4): # Busqueda correcta
                response['Marca'] = self.get_text('/html/body/table[1]/tbody/tr[1]/td[3]', 5)
                response['Modelo'] = self.get_text('/html/body/table[1]/tbody/tr[2]/td[2]', 5)
                response['Color'] = self.get_text('/html/body/table[1]/tbody/tr[1]/td[5]', 5)
                response['Año'] = self.get_text('/html/body/table[1]/tbody/tr[3]/td[2]', 5)
                response['Placa'] = id
                re = True
                status = 200
            else:
                re = True
                response['error'] = 'Placa not found'
        except Exception as e:
            print(e)
            re = False
            status = 500
        finally:
            self.wait = True
            return [re, response, status]

    def luz(self, p, op): # Main
        re = []
        response = {}
        status = 404
        if op == 'ci': fop = '1'
        elif op == 'contrato': fop = '3'
        else: fop = '2' # codigo
        try:
            self.wait = False
            self.driver.get(urlluzgye) # 
            self.select_input('//*[@id="vTIPODOCUMENTO"]', fop, 5) # Select option
            self.pass_text(p, '//*[@id="vNRODATO"]', 5, 0) # Input button 0. search by path
            self.button_click('//*[@id="TABLE4"]/tbody/tr[2]/td[2]/input', 5) # Search button
            if self.check_element('//*[@id="W0021Grid1ContainerRow_0001"]', 4): # Busqueda correcta
                response['Cliente'] = self.get_text('//*[@id="span_W0021vCLIENTESAPNOMBRE_0001"]/a', 5)
                response['Direccion'] = self.get_text('//*[@id="span_W0021vGRILLADIRECCION_0001"]', 5)
                response['Contrato'] = self.get_text('//*[@id="span_W0021vGCLIENTESAPCONTRATO_0001"]', 5)
                response['Codigo'] = self.get_text('//*[@id="span_W0021vGCLIENTESAPCUEN_0001"]', 5)
                response['Deduda'] = self.get_text('//*[@id="span_W0021vGRILLAMONTO_0001"]', 5)
                response['Ultimo Pago'] = self.get_text('//*[@id="span_W0021vFECHAULTPAGO_0001"]', 5)
                response['Vencimiento'] = self.get_text('//*[@id="span_W0021vFECHAVTO_0001"]', 5) 
                response['Nro Pendientes'] = self.get_text('//*[@id="W0021Grid1ContainerRow_0001"]/td[14]', 5) 
                re = True
                status = 200
            else:
                re = True
                response['error'] = 'Planilla not found'
        except Exception as e:
            print('--error-luz {}'.format(e))
            re = False
            status = 500
        finally:
            self.wait = True
            return [re, response, status]

    def cnt(self, p, op): # Main
        re = []
        response = {}
        status = 404
        if op == '1': fxpath = '//*[@id="scrcons"]/div[9]/div[2]/form/button' # Movil
        else: fxpath = '//*[@id="scrcons"]/div[9]/div[3]/form/button' # Fijo
        try:
            self.wait = False
            self.driver.get(urlluzgye) # 
            self.button_click(fxpath, 5) # Search button
            self.pass_text(p, '//*[@id="numserv"]', 5, 0) # Input button 0. search by path
            self.button_click('/html/body/div[1]/form/div[5]/div[2]/button', 5) # Search button
            if self.check_element('//*[@id="frmProcesa"]/div[1]/div[2]', 4): # Busqueda correcta
                response['Titular'] = self.get_value('//*[@id="frmProcesa"]/div[2]/div[2]/input', 5)
                response['CI-RUC'] = self.get_value('//*[@id="frmProcesa"]/div[4]/div[2]/input', 5)
                response['Numero'] = p
                response['Total'] = self.get_value('//*[@id="frmProcesa"]/div[8]/div[2]/input', 5)
                re = True
                status = 200
            else:
                re = True
                response['error'] = 'Planilla not found'
        except Exception as e:
            print('--error-cnt {}'.format(e))
            re = False
            status = 500
        finally:
            self.wait = True
            return [re, response, status]