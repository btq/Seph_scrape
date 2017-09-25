import time
import json
import requests
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from bs4 import BeautifulSoup

def parse_sephora_results_page(urlbase,page):
    if page==1:
        url = urlbase
    else:
        url = urlbase + '&currentPage=' + str(page)
    print 'Parsing ' + url
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"lxml")
    data = soup.find('script',attrs={'id':"searchResult"}).get_text()
    jsondata = json.loads(data)
    df=pd.DataFrame(jsondata['products']['products'])
    df['date_scraped']=datetime.now()
    return df

urlroot = 'http://www.sephora.com/search/search.jsp?keyword=hair&mode=all&node=1050092&sortBy=P_BEST_SELLING%3A1%3A%3AP_RATING%3A1%3A%3AP_PROD_NAME%3A0%3A%3AP_DEFAULT_SKU%3A1&pageSize=-1'
#todo: get page numbers from search results
for p in np.arange(1,5):
    page_df = parse_sephora_results_page(urlroot,p)
    tsleep=np.random.randn()+2
    if tsleep<0:
        tsleep=tsleep*-1
    print tsleep
    time.sleep(tsleep)
    if p==1:
        page_df['rank']=page_df.index+1
        seph_df = page_df
    else:
        page_df['rank']=page_df.index+seph_df.shape[0]+1
        seph_df = pd.concat([seph_df,page_df])

seph_df['pct_rank']=seph_df['rank'].div(seph_df.shape[0]).mul(100)
#Reorder columns
seph_df = seph_df[['date_scraped','rank','pct_rank','brand_name','display_name','rating','id','product_url']]

filename_out = 'files/sephora_hair_search_' + str(datetime.now().date()) + '.xlsx'
seph_df.to_excel(filename_out,index=False)
filename_out2 = 'files/briogeo_sephora_hair_search_' + str(datetime.now().date()) + '.xlsx'
seph_df[seph_df['brand_name']=='Briogeo'].to_excel(filename_out2,index=False)
