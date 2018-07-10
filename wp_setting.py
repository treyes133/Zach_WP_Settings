from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, traceback, threading


class wp_settings(threading.Thread):
	driver = None
	config = None
	address = None
	name = None
	
	count = 0
	
	
	#wifi - TF/Admin - TF/standby image/screen saver image
	settings = []
	setting_status = [False]*len(settings)
	
	state = False
	def __init__(self, addr, n, con):
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		#chrome_options.add_argument("--headless")
		chrome_options.add_argument("--test-type")
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument('--ignore-ssl-errors')
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		
		self.address = addr
		self.name = n
		self.config = con
		
		threading.Thread.__init__(self)
	def run(self):
		self.login()

	
		firmware = self.driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[11]/td/a")
		firmware.click()
		
		file_choose = self.driver.find_element_by_name("filename_conf")
		file_choose.send_keys(self.config)
		
		import_key = self.driver.find_element_by_name("load_cgi_config")
		import_key.click()
		
		self.accept_alert()
		
		print(self.name+" ip: "+ self.address+" has updated")
		self.state = True
	def accept_alert(self):
		try:
			WebDriverWait(self.driver, 3).until(EC.alert_is_present(),'Timed out waiting for PA creation confirmation popup to appear.')
			alert = self.driver.switch_to.alert
			alert.accept()
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
				
				password_field = self.driver.find_element_by_name("password")
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
settings_path = "C:\\Users\\coe-tomas.reyes\\Desktop\\settings.conf"

address = "128.194.61.192"
name = "93D"

wp_obj = wp_settings(address,name,settings_path)
wp_obj.start()
time_start = time.time()
while wp_obj.state is False:
	time.sleep(0.001)
time_end = time.time()
print("Total time :: "+str(time_end))