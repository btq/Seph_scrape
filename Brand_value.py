
# coding: utf-8

# In[1]:

import time
import json
import requests
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from bs4 import BeautifulSoup


# In[2]:

f='BestSellerBrioge20170722to20170805.xlsx'
sales_df=pd.read_excel(f)


# In[3]:

sales_df.head()


# In[4]:

sales_df.columns


# In[7]:

sales_df = sales_df[['New','SKU','SKU Desc','Retail','Sls U .COM']]
sales_df['NetSales$']=sales_df['Retail']*sales_df['Sls U .COM']
sales_df.head()


# In[ ]:



