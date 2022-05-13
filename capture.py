import time
import configparser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config_file = configparser.ConfigParser()
config_file.read("config.ini")
serverName = config_file["Setting"]["serverName"]
url = config_file["Setting"]["url"]
path = config_file["Setting"]["captureSavePath"]
second  = int(config_file["Setting"]["second"])

username = config_file["Setting"]["username"]
password = config_file["Setting"]["password"]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

print("Opening browser....")
driver.get(url)
time.sleep(2)

print("Login....")
driver.find_element(By.ID, 'login_username').send_keys(username)
driver.find_element(By.ID, 'login_password').send_keys(password)
driver.find_element(By.ID, 'login_right_submit_btn').click()
time.sleep(10)
driver.find_element(By.ID, 'clickAndRunIcon').click()
time.sleep(10)
driver.find_element(By.XPATH, "//span[text()='Launch Remote Console']").click()
time.sleep(15)
print("Waiting new tab load up")

p = driver.current_window_handle
parent = driver.window_handles[0]
driver.switch_to.window(driver.window_handles[1])
print("Current window title: " + driver.title)

print("Start capture screen every {} seconds".format(second))
while True:
    now = datetime.now()
    current_time = now.strftime("%Y%m%d-%H%M%S")
    print(current_time)

    el = driver.find_element(By.TAG_NAME, 'body')
    filename = ('{}{}-{}.png').format(path, current_time, serverName)
    print("Screen Captured: " + filename)
    el.screenshot(filename)
    time.sleep(second)
