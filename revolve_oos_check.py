
# coding: utf-8

# In[1]:


import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

url='http://www.revolve.com/briogeo/br/2e2c0b/'


# In[6]:


resp=requests.get(url)
soup=BeautifulSoup(resp.content,"lxml")


# In[7]:


hover_btns=soup.find_all('a',attrs={'class':"image-hover__btn image-hover__btn--focusable js-plp-quickview"})
hover_btns[0]


# In[8]:


[x['aria-label'] for x in hover_btns if x['aria-label'].count('PREORDER')]


# In[9]:


[x['aria-label'] for x in hover_btns if x['aria-label'].count('QUICK VIEW')]


# In[23]:


#prod_list=soup.find('ul',attrs={'id':"plp-prod-list"})
prod_list=soup.find_all('li',attrs={'class':"js-plp-container"})
print prod_list[0].prettify()
#prods=prod_list.find_all('div',attrs={'class':"plp_image_wrap"})
for p in prod_list:
    link=p.find('a',attrs={'class':"js-plp-pdp-link"})
    #print link["href"]
    hovr_btn=p.find('a',attrs={'class':"image-hover__btn image-hover__btn--focusable js-plp-quickview"})
    print hovr_btn.get_text(strip=True)
    #if hovr_btn['aria-label'].count('PREORDER'):
    if hovr_btn.get_text(strip=True)=='PREORDER':
        print "OOS: http://revolve.com"+link["href"]+' '+hovr_btn['aria-label'].replace('PREORDER','')


# In[28]:


prod_url='http://www.revolve.com/briogeo-rosarco-repair-conditioner/dp/BOGE-WU4/?product=BOGE-WU4'

resp_prod=requests.get(prod_url)
soup=BeautifulSoup(resp_prod.content,"lxml")

preord_button=soup.find('input',attrs={'id':"addtobagbutton_preorder"})

preord_button.attrs['style']==''


# In[27]:


prod_url='http://www.revolve.com/briogeo-scalp-revival-charcoal-tea-tree-scalp-treatment/dp/BOGE-WU12/?product=BOGE-WU12'

resp_prod=requests.get(prod_url)
soup=BeautifulSoup(resp_prod.content,"lxml")

preord_button=soup.find('input',attrs={'id':"addtobagbutton_preorder"})

preord_button.attrs['style']==''

