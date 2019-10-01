from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import sys

base_url='https://www.birchbox.com/'
url=f"https://www.birchbox.com/brand/4614" #BIRCHBOX

driver=webdriver.Firefox()
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"vertical__content___2lOQc"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

sys.stdout.flush()
#try:
driver.execute_script("window.scrollTo(0, 400);")
#print("scrolling")
#except 
time.sleep(1+np.abs(np.random.rand()))
driver.execute_script("window.scrollTo(0, 800);")
time.sleep(1+np.abs(np.random.rand()))
driver.execute_script("window.scrollTo(0, 1200);")
time.sleep(1+np.abs(np.random.rand()))
driver.execute_script("window.scrollTo(0, 1600);")
time.sleep(1+np.abs(np.random.rand()))
driver.execute_script("window.scrollTo(0, 2000);")
time.sleep(1+np.abs(np.random.rand()))
driver.execute_script("window.scrollTo(0, 2400);")
test=driver.find_elements_by_partial_link_text('Briogeo')
sys.stdout.flush()


print(len(test))

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
print(soup.contents)


link_list=[]
print(len(soup.find_all('a',attrs={'class':'productThumb__title___1D-Rj'})))
prod_thumb=soup.find_all('a',attrs={'class':'productThumb__title___1D-Rj'})
for this_one in prod_thumb:
  print(this_one.attrs['href'])
  print(this_one.text)
  link_list.append(base_url+this_one.attrs['href'])

for link in link_list:
  driver.get(link)
  try:
    wait=WebDriverWait(driver,delay)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"newProductCard_price__m3Jaa"))) #BIRCHBOX
    print("page is ready")
  except TimeoutException:
    print("Loading took too much time")
  bb_html = driver.execute_script("return document.body.outerHTML;")
  bb_soup=BeautifulSoup(bb_html,'lxml')
  print(bb_soup.contents)
