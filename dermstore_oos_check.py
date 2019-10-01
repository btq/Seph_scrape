
# coding: utf-8

# In[7]:


import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText


# In[8]:


resp=requests.get('https://www.dermstore.com/profile_Briogeo_502970.htm')
soup=BeautifulSoup(resp.content,"lxml")
print soup.prettify()
#output=json.loads(resp.text)

#souper=BeautifulSoup(output['products'],"lxml")
#print souper
#for d in output:
#    print d


# In[3]:


prod_list=souper.find_all('a',attrs={'title':"Notify Me"})
prod_list

