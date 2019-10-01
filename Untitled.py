
# coding: utf-8

# In[1]:


import json
import requests
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request
import requests


# In[2]:


urlroot='https://sephora.com'
prod_urls=['/product/superfoods-shampoo-conditioner-hair-pack-P431542',
'/product/dont-despair-repair-deep-conditioning-mask-P388628',
'/product/scalp-revival-charcoal-coconut-oil-micro-exfoliating-shampoo-P418507',
'/product/rosarco-milk-reparative-leave-in-conditioning-spray-P396733',
'/product/be-gentle-be-kind-matcha-apple-replenishing-superfood-shampoo-P431543',
'/product/scalp-revival-charcoal-tea-tree-scalp-treatment-P418506',
'/product/be-gentle-be-kind-kale-apple-replenishing-superfood-conditioner-P431544',
'/product/don-t-despair-repair-strength-moisture-leave-in-mask-P427526',
'/product/don-rsquo-t-despair-repair-tm-deep-conditioning-mask-mini-P426204',
'/product/don-t-despair-repair-super-moisture-shampoo-P427718',
'/product/rosarco-blow-dry-perfection-heat-protectant-creme-P411359',
'/product/blossom-bloom-ginseng-biotin-volumizing-shampoo-P402071',
'/product/rosarco-repair-conditioner-P402073',
'/product/blossom-bloom-ginseng-biotin-volumizing-conditioner-P388625',
'/product/dont-despair-repair-deep-conditioning-hair-cap-system-P425409',
'/product/scalp-revival-charcoal-peppermint-oil-cooling-jelly-conditioner-P429961',
'/product/scalp-revival-charcoal-biotin-dry-shampoo-P418505',
'/product/curl-charisma-rice-amino-avocado-leave-in-defining-creme-P388626',
'/product/blossom-bloom-ginseng-biotin-volumizing-spray-P396734',
'/product/blossom-bloom-volumizing-on-the-go-travel-kit-P422370',
'/product/be-gentle-be-kind-avocado-quinoa-co-wash-P388623',
'/product/rosarco-repair-shampoo-P402072',
'/product/scalp-revival-scalp-massager-P429962',
'/product/curl-charisma-definition-on-the-go-travel-kit-P422368',
'/product/curl-charisma-rice-amino-shampoo-P402074',
'/product/rosarco-oil-P388629',
'/product/curl-charisma-rice-amino-shea-curl-defining-conditioner-P388627',
'/product/scalp-revival-charcoal-coconut-oil-micro-exfoliating-shampoo-mini-P427715',
'/product/curl-charisma-rice-amino-quinoa-frizz-control-gel-P408411',
'/product/don-t-despair-repair-gel-to-oil-overnight-repair-treatment-P408248',
'/product/rosarco-milk-tm-reparative-leave-in-conditioning-spray-mini-P426205',
'/product/rosarco-repair-on-the-go-travel-kit-P422369']


# In[8]:


brand_page='https://www.sephora.com/brand/briogeo'
brand_page='https://www.sephora.com/product/don-t-despair-repair-strength-moisture-leave-in-mask-P427526'


# In[10]:


#driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
#delay=10

driver.get(brand_page)
try:
  wait=WebDriverWait(driver,delay)
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"css-0"))) #sephora
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")


# In[12]:


html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
print(soup.contents)


# In[13]:


data = soup.find('script',attrs={'id':"linkJSON"}).get_text()
output = json.loads(data)


# In[14]:


print(output)


# In[19]:


for d in output:
  print(d.keys())
  print(d['path'])
  if d['path']=='RegularProductTop':
    prod=d['props']['currentProduct']
    if 'regularChildSkus' in prod.keys():
      field='regularChildSkus'
      for sku in prod[field]:
        print(sku['targetUrl'], sku['skuName'], ' OOS:', sku['isOutOfStock'], ' FewLeft:', sku['isOnlyFewLeft'])
#        if sku['isOutOfStock']:
#                            oos_flag=True
#                            text_file.write("\nOOS: {0} {1}\n".format(urlroot+sku['targetUrl'], sku['skuName']))
#        if sku['isOnlyFewLeft']:
#                            oos_flag=True
#                            text_file.write("\mFEW_LEFT: {0} {1}\n".format(urlroot+sku['targetUrl'], sku['skuName']))
    else:
      field='currentSku'
      sku=prod[field]
      print(sku['targetUrl'], ' OOS:', sku['isOutOfStock'], ' FewLeft:', sku['isOnlyFewLeft'])
#                    if sku['isOutOfStock']:
#                        oos_flag=True
#                        text_file.write("\nOOS: {0}\n".format(urlroot+sku['targetUrl']))
#                    if sku['isOnlyFewLeft']:
#                        oos_flag=True
#                        text_file.write("\nFEW_LEFT: {0}\n".format(urlroot+sku['targetUrl']))

