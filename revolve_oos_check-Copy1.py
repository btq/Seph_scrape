
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


# In[43]:


resp=requests.get(url)
soup=BeautifulSoup(resp.content,"lxml")


# In[52]:


prod_list=soup.find('ul',attrs={'id':"plp-prod-list"})
prod_list


# In[60]:


hover_btns=soup.find_all('a',attrs={'class':"image-hover__btn image-hover__btn--focusable js-plp-quickview"})
hover_btns[0]


# In[59]:


[x['aria-label'] for x in hover_btns if x['aria-label'].count('PREORDER')]


# In[61]:


[x['aria-label'] for x in hover_btns if x['aria-label'].count('QUICK VIEW')]


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

