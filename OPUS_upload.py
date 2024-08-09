###Save the webdriver and  script under one folder. 
##By Lin  20170308. 
#Path of the webdriver. 
#PathProgram="C:/Users/lxiong/UMD/GPS/data"
#find your data file folder. 
Path="C:/Users/lxiong/UMD/GPS/data"
#File format 
fileformat="*.23o"
 
#Antenna height 
height=0.0 
email="gpsandlidar2018@gmail.com"
antenna="TRM57971.00     NONE"
#antenna="TRMR10          NONE" 
 
import glob, os, time 
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import UnexpectedAlertPresentException 
from selenium.common.exceptions import NoAlertPresentException 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
 
def upload(): 
    time.sleep(1) 
    try: 
        driver.find_element(By.CLASS_NAME, "declineButton").click()

 
    except NoSuchElementException: 
         print ("No survey pop up!") 
 
    elem = driver.find_element(By.NAME, "uploadfile") 
    elem.clear() 
    elem.send_keys("{}".format(filepath)) 
    driver.find_element(By.XPATH, "//*[@id='container']/form/div[1]/span").click()
    time.sleep(2) 
    user_input = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
 
    user_input.send_keys(antenna) 
    time.sleep(2) 
    driver.find_element(By.CSS_SELECTOR, "#select2-ant_type-results > li:nth-child(1)").click()

    elem = driver.find_element(By.NAME, "height")

    elem.clear() 
    elem.send_keys("{}".format(height)) 
    elem = driver.find_element(By.NAME, "email_address")

    elem.clear() 
    elem.send_keys("{}".format(email)) 
    elem.send_keys(Keys.RETURN) 
    #driver.find_element(By.ID, "Rapid-Static").click()
    driver.find_element(By.ID, "Static").click()
 
    try: 
       WebDriverWait(driver, 2).until(EC.alert_is_present()) 
       alert = driver.switch_to_alert() 
       alert.accept() 
    except TimeoutException: 
       print ("No antenna height alert!") 
    time.sleep(1) 
    driver.back() 
 
 
# "{}/chromedriver".format(PathProgram) 

driver = webdriver.Chrome() 
driver.get("http://www.ngs.noaa.gov/OPUS/") 
 
os.chdir("{}".format(Path)) 
count=0 
for file in glob.glob(fileformat): 
   print ("UploadFile:  ", os.path.abspath(file)) 
   filepath="{}".format(os.path.abspath(file)) 
   # Count time 
   start_time = time.time() 
   try: 
       upload() 
   except (TimeoutException,UnexpectedAlertPresentException,NoAlertPresentException,NoSuchElementException) as e: 
 
       print ("Webpage no response ") 
       time.sleep(10) 
       driver.execute_script("window.open('http://www.google.com');") 
       time.sleep(2) 
       driver.switch_to.window(driver.window_handles[1]) 
       driver.get("http://www.ngs.noaa.gov/OPUS/") 
       upload() 
   count=count+1 
   print ("Number of Uploaded Files: ",count) 
   print ('Uploading time(second) is ', time.time() - start_time) 
   time.sleep(2) 
   #print ('Remove File') 
   #os.remove(file) 
driver.quit()
