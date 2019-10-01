from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request
import sys
import time
import json

template:
OOS Alert
# Stores
# Skus

Store1
Skus w/ links

Store2
skus w/ links


architecture:
Loop through stores, with urls.
Parse Brand page (and get OOS from that if possible)
Parse each product page
When OOS, write to dict:
store
sku
link
write report-
count stores in dict
count skus in dict
write out skus for each store
send

class StoreOOS(object):
	""" Store out of stock class """
	def __init__(self, sitename='SephoraUSA', siteurl='https://sephora.com'):
		self.sitename=sitename
		self.siteurl=siteurl

	def getBrandPage(self):
		case 



def BirchBoxBrandPage(url,oos_list):
	url=f"https://www.birchbox.com/brand/4614" #BIRCHBOX
    driver=webdriver.Firefox()
    #driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
    delay=10
    driver.get(url)
    try:
    	wait=WebDriverWait(driver,delay)
    	# DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
    	wait.until(EC.presence_of_element_located((By.CLASS_NAME,"vertical__content___2lOQc"))) #BIRCHBOX
    	print("page is ready")
    except TimeoutException:
    	print("Loading took too much time")

    driver.execute_script("window.scrollTo(0, 400);")
    #print("scrolling")
    #except 
    while scrollY<2400:
      time.sleep(np.random.rand()+1)
      driver.execute_script("window.scrollTo(0, {0});".format(scrollY))
      scrollY+=400

    #test=driver.find_elements_by_partial_link_text('Briogeo')
    
    html = driver.execute_script("return document.body.outerHTML;")
    soup=BeautifulSoup(html,'lxml')

    base_url='https://www.birchbox.com/'
    prod_thumb=soup.find_all('a',attrs={'class':'productThumb__title___1D-Rj'})
    for this_one in prod_thumb:
      #this_one=prod_thumb[0]
      print(base_url+this_one.attrs['href'])
      print(this_one.text)



def RileyRoseBrandPage(url,oos_list):
	rr_url=f"https://www.rileyrose.com/us/shop/catalog/category/rr/promo-branded-briogeo"
    rr_html_page=requests.get(rr_url)
    rr_soup=BeautifulSoup(rr_html_page.content,'lxml')
    rr_scripts=rr_soup.find_all('script',attrs={'type':'text/javascript'})
    start_pos=rr_scripts[-1].text.find('var cData =')
    end_pos=rr_scripts[-1].text.find('"};',start_pos)
    jsondata = json.loads(rr_scripts[-1].text[start_pos+12:end_pos+2])
    for p in jsondata['CatalogProducts']:
    	print(p['DisplayName'], p['IsOOS'])
    	if p['IsOOS']==True:
    		oos_list.append(('RileyRose',p['DisplayName'],p['ProductShareLinkUrl']))
    return oos_list

