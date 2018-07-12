from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, traceback, threading,sys
import os



class wp_settings(threading.Thread):
	driver = None
	address = None
	name = None
	
	count = 0

	
	state = False
	def __init__(self, addr, n):
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--test-type")
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument('--ignore-ssl-errors')
		self.driver = webdriver.Chrome(chrome_options=chrome_options)

		#os.environ['MOZ_HEADLESS'] = '1'
		#self.driver = webdriver.Firefox()

		
		
		self.address = addr
		self.name = n
		
		threading.Thread.__init__(self)
	def run(self):
		count = 0
		desktop = os.path.expanduser("~\\Desktop\\Zach_WP\\")
		self.login()
		osd_setup = self.driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[6]/td/a")
		osd_setup.click()
		
		file_upload = self.driver.find_element_by_name("filename")
		file_upload.send_keys(desktop+"file.png")

		file_upload = self.driver.find_element_by_name("imgsubmit")
		file_upload.click()

		self.accept_alert(False)

		screen_saver = self.driver.find_element_by_name("logoname")
		screen_saver.send_keys(desktop+"screensaver.png")
	
		logo_submit = self.driver.find_element_by_name("logosubmit")
		logo_submit.click()
		
		self.accept_alert(False)
		
	
		firmware = self.driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[11]/td/a")
		firmware.click()

		
		
		file_choose = self.driver.find_element_by_name("filename_conf")
		file_choose.send_keys(desktop+"settings.conf")
		
		import_key = self.driver.find_element_by_name("load_cgi_config")
		import_key.click()
		
		self.accept_alert(True)
		
		
		print(self.name+" ip: "+ self.address+" has updated")
		self.state = True
	def accept_alert(self,value):
		try:
			WebDriverWait(self.driver, 3).until(EC.alert_is_present(),'Timed out waiting for PA creation confirmation popup to appear.')
			alert = self.driver.switch_to.alert
			if(value):
				alert.accept()
			else:
				alert.dismiss()
			print("alert accepted")
		except TimeoutException:
			print("no alert")
		
	def login(self):
		logged = False
		
		while not logged:
			try:
				self.driver.get("http://"+self.address+"/")
				admin_button = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/a')
				admin_button.click()

				time.sleep(0.001)
				
				password_field = self.driver.find_element_by_xpath("/html/body/div/div[3]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input")
				password_field.send_keys("admin")
				
				login_button = self.driver.find_element_by_name("Login")
				login_button.click()
				
				logged = True
			except:
				print("error logging in, trying again in 5 seconds")
				self.driver.save_screenshot(str(self.count)+".png")
				time.sleep(5)
				traceback.print_exc()
				self.count += 1
		self.page = "home"

address = "128.194.61.192"
name = "93D"

wp_obj = wp_settings(address,name)
wp_obj.start()
time_start = time.time()
while wp_obj.state is False:
	time.sleep(0.001)
time_end = time.time()
print("Total time :: "+str(time_end-time_start))
