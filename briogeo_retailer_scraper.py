import os
import re
import time
import utils
import mail
import json
import requests
import collections
import pandas as pd
from utils import log
from datetime import datetime
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from http.client import RemoteDisconnected
import numpy as np

import urllib3
urllib3.disable_warnings()

retailer_urls_all={
  "Sephora USA": f"http://www.sephora.com"
  ,"Sephora CAN": f"http://www.sephora.com/ca/en"
  ,"Sephora France": f"https://www.sephora.fr"
  ,"Sephora Middle East": f"https://www.sephora.ae"
  ,"Sephora SE Asia": f"http://www.sephora.sg"
  ,"Sephora Thailand": f"https://www.sephora.co.th"
  ,"Sephora AUS": f"http://www.sephora.com.au"
  ,"Revolve": f"http://www.revolve.com"
  ,"Riley Rose": f"https://www.rileyrose.com"
  ,"Birchbox": f"http://www.birchbox.com"
  ,"Nordstrom": f"http://shop.nordstrom.com"
  ,"Net-A-Porter": f"https://www.net-a-porter.com"
  ,"Beauty Bay": f"https://www.beautybay.com"
  ,"Beauty Bay 2": f"https://www.beautybay.com"
  ,"Cult Beauty": f"https://www.cultbeauty.co.uk"
  ,"Anthropologie": f"https://www.anthropologie.com"
  ,"Free People": f"https://www.freepeople.com"
  ,"I Am Natural Store": f"https://www.iamnaturalstore.com.au"
  ,"Urban Outfitters": f"https://www.urbanoutfitters.com"
#  ,"Naturisimo": f"https://www.naturisimo.com/"
}
df_root_urls=pd.DataFrame(list(zip(retailer_urls_all.keys(),retailer_urls_all.values())),columns=['Retailer','root_url'])

brand_pages_all={
  "Sephora USA": f"http://www.sephora.com/brand/briogeo/all"
  ,"Sephora CAN": f"http://www.sephora.com/ca/en/brand/briogeo/all"
  ,"Sephora France": f"https://www.sephora.fr/marques/de-a-a-z/briogeo-briog/"
  ,"Sephora Middle East": f"https://www.sephora.ae/en/brands/briogeo"
  ,"Sephora SE Asia": f"http://www.sephora.sg/brands/briogeo?view=120"
  ,"Sephora Thailand": f"https://www.sephora.co.th/brands/briogeo?view=120"
  ,"Sephora AUS": f"https://www.sephora.com.au/brands/briogeo?view=60"
  ,"Revolve": f"http://www.revolve.com/briogeo/br/2e2c0b/"
  ,"Riley Rose": f"https://www.rileyrose.com/us/shop/catalog/category/rr/promo-branded-briogeo"
  ,"Birchbox": f"http://www.birchbox.com/brand/4614"
  ,"Nordstrom": f"https://shop.nordstrom.com/c/briogeo?origin=productBrandLink"
  ,"Net-A-Porter": f"https://www.net-a-porter.com/us/en/Shop/Designers/Briogeo?pn=1&npp=60&image_view=product&dScroll=0"
  ,"Beauty Bay": f"https://www.beautybay.com/l/briogeo/"
  ,"Beauty Bay 2": f"https://www.beautybay.com/l/briogeo/?f_pg=2"
  ,"Cult Beauty": f"https://www.cultbeauty.co.uk/briogeo"
  ,"Anthropologie": f"https://www.anthropologie.com/beauty-hair-care?brand=Briogeo"
  ,"Free People": f"https://www.freepeople.com/brands/briogeo/"
  ,"I Am Natural Store": f"https://www.iamnaturalstore.com.au/collections/briogeo"
  ,"Urban Outfitters": f"https://www.urbanoutfitters.com/brands/briogeo"
#  ,"Naturisimo": f"https://www.naturisimo.com/index.cfm?nme=bri"
}

class BriogeoRetailerScraper(object):
  def __init__(self, retailers=brand_pages_all.keys(), send_email=True, from_email='briogeods@gmail.com', to_email='btquinn@gmail.com', update_db=True):
    
    if not isinstance(retailers, collections.KeysView):
      self.brand_pages=dict(zip(retailers,[brand_pages_all.get(x) for x in retailers]))
    else:
      self.brand_pages=brand_pages_all

    keys_to_remove=[k for k,v in self.brand_pages.items() if v is None]
    for k in keys_to_remove:
      log.warn('Retailer {} not in retailer dictionary. Removed.'.format(k))
      self.brand_pages.pop(k)
    if len(self.brand_pages)==0:
      log.error('List of retailers provided was invalid/empty.')

    self.send_email = send_email
    self.update_db = update_db
    self.driver = None
    self.delay = 10
    self.from_email = from_email
    self.to_email = to_email

    self.soup = []
    self.df_prod_pages = pd.DataFrame()

  def load_page_requests(self,url):
    time.sleep(1+np.abs(np.random.rand()))
    try:
      resp=requests.get(url,verify=False)
    except (requests.HTTPError, requests.ConnectionError):
      #os.remove(email_filename)
      #raise
      log.warn('Could not connect to {}'.format(url))
    self.soup = BeautifulSoup(resp.content,"lxml")

  def load_page_selenium(self,url,by_cont,by_name,scroll=False,click=False,click_xpath=''):
    if not self.driver:
      self.driver=webdriver.Firefox()
    try:
      self.driver.get(url)
    except ConnectionResetError:
      print('ConnectionResetError 111')
      time.sleep(3.5)
      self.driver.get(url)
    except BrokenPipeError:
      print('BrokenPipeError 115')
      try:
        self.driver.close()
      except ConnectionResetError:
        print('ConnectionResetError 119')
        self.driver.close()
      self.driver=None
      self.driver=webdriver.Firefox()
      time.sleep(2)
      self.driver.get(url)
    try:
      wait=WebDriverWait(self.driver,self.delay)
      wait.until(EC.presence_of_element_located((by_cont,by_name)))
      print("page is ready")
    except TimeoutException:
      print("Loading took too much time")
    if scroll==True:
      scroll_height=self.driver.execute_script("return document.body.scrollHeight;")
      scroll_to=300
      loop_limit=30
      loop_cnt=1
      while scroll_to < scroll_height:
        if loop_cnt>loop_limit:
          break
        self.driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
        time.sleep(0.8+np.abs(np.random.rand()))
        scroll_height=self.driver.execute_script("return document.body.scrollHeight;")
        scroll_to+=300
        loop_cnt+=1
      self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(1.5+np.abs(np.random.rand()))
    if click==True:
      click_link=self.driver.find_element_by_xpath(click_xpath)
      click_link.click()
    time.sleep(3)
    try:
      html = self.driver.execute_script("return document.body.outerHTML;")
    except RemoteDisconnected:
      print('RemoteDisconnected 153')
      time.sleep(2)
      html = self.driver.execute_script("return document.body.outerHTML;")
    except ConnectionResetError:
      print('ConnectionResetError 156')
      time.sleep(1)
      html = self.driver.execute_script("return document.body.outerHTML;")
    self.soup=BeautifulSoup(html,'lxml')

  def load_and_parse_all_brand_pages(self):
    for r in self.brand_pages.keys():
      self.load_brand_page(r)
      self.parse_brand_page_soup(r)
    if 'Beauty Bay 2' in self.df_prod_pages['Retailer'].unique().tolist():
      self.df_prod_pages.loc[self.df_prod_pages['Retailer']=='Beauty Bay 2','Retailer']='Beauty Bay'

  def load_brand_page(self,retailer):
    brand_page=self.brand_pages[retailer]
    print('Loading {} brand page: {}'.format(retailer,brand_page))
    if retailer in ['Sephora USA','Sephora CAN','Sephora France','Sephora Middle East','Nordstrom','Riley Rose','Revolve']:
      self.load_page_requests(brand_page)
    elif retailer in ['Sephora SE Asia','Sephora Thailand','Sephora AUS']:
      self.load_page_selenium(brand_page,By.ID,"product-index-content")
    elif retailer == 'Cult Beauty':
      self.load_page_selenium(brand_page,By.CLASS_NAME,"col mainContent",scroll=False,click=True,click_xpath="/html/body/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[3]/button")
    elif retailer == 'Birchbox':
      self.load_page_selenium(brand_page,By.CLASS_NAME,"vertical__content___2lOQc",scroll=True,click=True,click_xpath="//button[1]")
    elif retailer == 'Net-A-Porter':
      self.load_page_selenium(brand_page,By.ID,'page-container',scroll=True)
    elif retailer in ['Beauty Bay','Beauty Bay 2']:
      self.load_page_selenium(brand_page,By.CLASS_NAME,"c-product qa-product",scroll=True)
    elif retailer == 'Anthropologie':
      self.load_page_selenium(brand_page,By.CLASS_NAME,"dom-category-browse",scroll=True)
    elif retailer == 'Free People':
      self.load_page_selenium(brand_page,By.CLASS_NAME,"dom-product-tile",scroll=True)
    elif retailer == 'I Am Natural Store':
      self.load_page_selenium(brand_page,By.CLASS_NAME,"inner-top",scroll=True)#,click=True,click_xpath='//a[@data-translate="collections.general.show_more"]')
    elif retailer == 'Urban Outfitters':  
      self.load_page_selenium(brand_page,By.CLASS_NAME,'dom-product-tile')
    elif retailer == 'Naturisimo':
      self.load_page_selenium(brand_page,By.CLASS_NAME,'product_box')


  def parse_brand_page_soup(self,retailer):
    soup=self.soup
    
    ### SEPHORA USA
    ### SEPHORA CANADA
    if retailer in ['Sephora USA','Sephora CAN']:
      data = soup.find('script',attrs={'id':"linkJSON"}).get_text()
      output = json.loads(data)
      for d in output:
        if d['path']=='CatalogPage':
          prods=d['props']['products']
          df=pd.DataFrame(d['props']['products'])
          #pd.DataFrame(list(df['currentSku'].to_dict().values()))['listPrice']
          df['Retailer']=retailer
          df['OOS_FewLeft']='No'
          if retailer=='Sephora CAN':
            df['targetUrl']=df['targetUrl'].transform(lambda x: retailer_urls_all[retailer]+x+'?country_switch=ca&lang=en')
          else:
            df['targetUrl']=df['targetUrl'].transform(lambda x: retailer_urls_all[retailer]+x)
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### SEPHORA FRANCE
    elif retailer == 'Sephora France':
      prod_divs = soup.find_all('div',attrs={'class':"product-tile clickable"})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_divs:
        p_json = json.loads(p['data-tcproduct'])
        if p_json is not None:
          if p_json['product_brand']=='BRIOGEO':
            prod_name_list.append(p_json['product_pid_name'])
            prod_url_list.append(p_json['product_url_page'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### SEPHORA MIDDLE EAST
    elif retailer in ['Sephora Middle East']:
      ae_ul=soup.find('ul',attrs={'class':"products-grid products-grid--max-4-col"})
      ae_tags=ae_ul.find_all('a',attrs={'class':'product-image'})
      prod_name_list=[]
      prod_url_list=[]
      for p in ae_tags:
        prod_name_list.append(p['title'])
        prod_url_list.append(p['href'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### SEPHORA SOUTH EAST ASIA
    ### SEPHORA THAILAND
    ### SEPHORA AUSTRALIA
    elif retailer in ['Sephora SE Asia','Sephora Thailand','Sephora AUS']:
      prod_ind=soup.find('div',attrs={'class':'products-grid'})
      prods=prod_ind.find_all('div',attrs={'class':'product-card'})
      prod_name_list=[]
      prod_url_list=[]
      prod_oos_list=[]
      for p in prods:
        prod_name_list.append(p.find('p',attrs={'class':'product-card-product'}).text)
        prod_url_list.append(retailer_urls_all[retailer]+p.find('a',attrs={'class':'product-card-description'})['href'])
        if p.find('div',attrs={'class':'out-of-stock'}):
          prod_oos_list.append('OOS')
        else:
          prod_oos_list.append('No')
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list,prod_oos_list)),columns=['displayName','targetUrl','OOS_FewLeft'])
      df['Retailer']=retailer
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### NORDSTROM
    elif retailer == 'Nordstrom':
      nd_start_pos=soup.text.find('__INITIAL_CONFIG__ = {')
      #nd_end_pos=soup.text.find('Server":true}}',nd_start_pos)
      #nd_jsondata=json.loads(soup.text[nd_start_pos+21:nd_end_pos+14])
      nd_end_pos=soup.text.find('webExtractor":{}}',nd_start_pos)
      nd_jsondata=json.loads(soup.text[nd_start_pos+21:nd_end_pos+17])
      prod_name_list=[]
      prod_url_list=[]
      for num,p in enumerate(nd_jsondata['viewData']['productsById'].keys(),1):
        prod_name_list.append(nd_jsondata['viewData']['productsById'][p]['name'])
        prod_url_list.append(retailer_urls_all[retailer]+nd_jsondata['viewData']['productsById'][p]['productPageUrl'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### RILEY ROSE
    elif retailer == 'Riley Rose':
      rr_scripts=soup.find_all('script',attrs={'type':'text/javascript'})
      ### TO DO: MAKE THIS A SEARCH THROUGH SCRIPTS FOR VAR CDATA
      rr_start_pos=rr_scripts[-2].text.find('var cData =')
      rr_end_pos=rr_scripts[-2].text.find('"};',rr_start_pos)
      rr_jsondata = json.loads(rr_scripts[-2].text[rr_start_pos+12:rr_end_pos+2])
      prod_name_list=[]
      prod_url_list=[]
      prod_oos_list=[]
      for p in rr_jsondata['CatalogProducts']:
        prod_name_list.append(p['DisplayName'])
        prod_url_list.append(p['ProductShareLinkUrl'])
        n_left=int(p['Variants'][0]['Sizes'][0]['LowStockMessage'])
        if p['IsOOS']==False and n_left>10:
          oos_value='No'
        elif n_left<=10:
          oos_value='{} Left'.format(n_left)
        else:
          oos_value='OOS'
        prod_oos_list.append(oos_value) 
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list,prod_oos_list)),columns=['displayName','targetUrl','OOS_FewLeft'])
      df['Retailer']=retailer
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### REVOLVE
    elif retailer == 'Revolve':
      prod_list=soup.find_all('li',attrs={'class':"js-plp-container"})
      prod_name_list=[]
      prod_url_list=[]
      prod_oos_list=[]
      for p in prod_list:
        link=p.find('a',attrs={'class':"js-plp-pdp-link"})
        hovr_btn=p.find('a',attrs={'class':"image-hover__btn image-hover__btn--focusable js-plp-quickview"})
        name=re.split(r"^PREORDER |^QUICK VIEW |^SOLD OUT ",hovr_btn['aria-label'])[1]
        #print(link["href"], hovr_btn['aria-label'])
        if hovr_btn.get_text(strip=True)=='PREORDER' or hovr_btn.get_text(strip=True)=='SOLD OUT':
          oos_value='OOS'
        else:
          oos_value='No'
        prod_name_list.append(name)
        prod_url_list.append(retailer_urls_all[retailer]+link['href'])
        prod_oos_list.append(oos_value)
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list,prod_oos_list)),columns=['displayName','targetUrl','OOS_FewLeft'])
      df['Retailer']=retailer
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### BIRCHBOX
    elif retailer == 'Birchbox':
      prod_list=soup.find_all('a',attrs={'class':'productThumb__title___1D-Rj'})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_list:
        if 'href' in p.attrs.keys():
          prod_name_list.append(p.text)
          prod_url_list.append(retailer_urls_all[retailer]+p['href'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### NET-A-PORTER
    elif retailer == 'Net-A-Porter':
      prod_list=soup.find_all('div',attrs={'class':'product-image'})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_list:
        prod_name_list.append(p.find('a').find('img')['alt'])
        prod_url_list.append(retailer_urls_all[retailer]+p.find('a')['href'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### BEAUTY BAY
    elif retailer in ['Beauty Bay','Beauty Bay 2']:
      prod_list=soup.find_all('a',attrs={'class':'c-product qa-product'})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_list:
        prod_name_list.append(p.find('img')['alt'])
        prod_url_list.append(retailer_urls_all[retailer]+p['href'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### CULT BEAUTY
    elif retailer == 'Cult Beauty':
      prod_list=soup.find_all('div',attrs={'class':'productGridItem'})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_list:
        prod_name_list.append(p['data-name'])
        long_url=p.find('a')['href']
        end_url_loc=long_url.find('.html#')
        prod_url_list.append(retailer_urls_all[retailer]+long_url[0:end_url_loc+5])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### ANTHROPOLOGIE
    elif retailer == 'Anthropologie':
      prod_list=soup.find_all('a',attrs={'class':'c-product-tile__image-link js-product-tile__image-link'})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_list:
        img=p.find('img')
        prod_name_list.append(img['alt'])
        prod_url_list.append(retailer_urls_all[retailer]+p['href'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### FREE PEOPLE
    elif retailer == 'Free People':
      prod_list=soup.find_all('div',attrs={'class':'dom-product-tile'})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_list:
        prod_name_list.append(p.find('meta',attrs={'itemprop':'name'})['content'])
        prod_url_list.append(p.find('meta',attrs={'itemprop':'url'})['content'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### I AM NATURAL STORE
    elif retailer == 'I Am Natural Store':
      prod_list=soup.find_all('div',attrs={'class':'inner-top'})
      prod_name_list=[]
      prod_url_list=[]
      prod_oos_list=[]
      for p in prod_list:
        oos_value=''
        prod_url_list.append(retailer_urls_all[retailer]+p.find('a')['href'])
        prod_name_list.append(p.find('a').find('img')['alt'].replace('<br>',''))
        prod_dat = json.loads(p.find('a',attrs={'title':'Quick View'})['data-istockvariants'])
        if len(prod_dat)>1:
          for x in range(len(prod_dat)):
            if prod_dat[x]['inventory_quantity']==0:
              oos_value+=(' {} OOS'.format(prod_dat[x]['title']))
        else:
          if prod_dat[0]['inventory_quantity']==0:
            oos_value='OOS'
          else:
            oos_value='No'
        prod_oos_list.append(oos_value) 
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list,prod_oos_list)),columns=['displayName','targetUrl','OOS_FewLeft'])
      df['Retailer']=retailer
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]

    ### URBAN OUTFITTERS
    elif retailer == 'Urban Outfitters':
      prod_list=self.soup.find_all('span',attrs={'itemprop':'product'})
      prod_name_list=[]
      prod_url_list=[]
      for p in prod_list:
        prod_url_list.append(p.find('meta',attrs={'itemprop':'url'})['content'])
        prod_name_list.append(p.find('meta',attrs={'itemprop':'name'})['content'])
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list)),columns=['displayName','targetUrl'])
      df['Retailer']=retailer
      df['OOS_FewLeft']='No'
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]
    
    ### NATURISIMO
    elif retailer == 'Naturisimo':
      prod_list=self.soup.find_all('div',attrs={'class':'product_box'})
      prod_name_list=[]
      prod_url_list=[]
      prod_oos_list=[]
      for p in prod_list:
        prod_url_list.append(retailer_urls_all[retailer]+p.find('a')['href'])
        prod_name_list.append(p.find('div',attrs={'class':'product_name'}).text)
        if p.find('form'):
          prod_oos_list.append('No')
        else:
          prod_oos_list.append('OOS')
      df=pd.DataFrame(list(zip(prod_name_list,prod_url_list,prod_oos_list)),columns=['displayName','targetUrl','OOS_FewLeft'])
      df['Retailer']=retailer
      df_brandpage_prods=df[['Retailer','displayName','targetUrl','OOS_FewLeft']]



    self.df_prod_pages=pd.concat([self.df_prod_pages,df_brandpage_prods],ignore_index=True)
  
  def remove_products(self):
    print('Removing Rosarco™ Blow Dry Perfection Heat Protectant Crème from product list.')
    self.df_prod_pages=self.df_prod_pages[~self.df_prod_pages.displayName.isin(['Rosarco Blow Dry Perfection & Heat Protectant Crème','Rosarco™ Blow Dry Perfection Heat Protectant Crème','Rosarco Blow Dry Perfection Heat Protectant Crème - Crème Cheveux Protectrice','Rosarco™ Blow Dry Perfection & Heat Protectant Crème'])]
    print('Removing Rosarco Repair Shampoo & Conditioner')
    rosarco_list=['ROSARCO  Repair Conditioner, 236ml', 'Rosarco™ Repair Conditioner', 'Rosarco Repair Shampoo Liter', 'Briogeo\xa0Rosarco Repair Shampoo, 240ml', 'Briogeo\xa0Rosarco Repair Conditioner, 240ml', 'Rosarco Repair On-The-Go Travel Kit', 'ROSARCO  Repair Shampoo, 236ml', 'Rosarco™ Repair Shampoo', 'Rosarco Repair Conditioner - Après-shampooing Réparateur', 'Rosarco Repair Conditioner', 'Briogeo Rosarco Repair Conditioner', 'Rosarco Repair Shampoo - Shampooing Réparateur', 'Briogeo Rosarco Repair Shampoo']
    self.df_prod_pages=self.df_prod_pages[~self.df_prod_pages.displayName.isin(rosarco_list)]
    print('Removing Rosarco Milk')
    rosarco_milk_list=['Briogeo Rosarco Milk Leave-In Conditioning Spray', 'Rosarco Milk™ Reparative Leave-In Conditioning Spray', 'ROSARCO MILK  Reparative Leave-in Conditioning Spray', 'Briogeo Farewell Frizz™ Rosarco Milk Leave-In Conditioning Spray', 'Farewell Frizz Rosarco Milk Leave-In Conditioning Spray', 'Briogeo\xa0Rosarco Milk Reparative Leave-In Conditioning Spray, 150ml', 'Briogeo Rosarco Milk Reparative Leave-In Conditioning Spray', 'Rosarco Milk Reparative Leave-In Conditioning Spray', 'Rosarco Milk Reparative Leave-In Conditioning Spray - Brume Revitalisante', 'Rosarco Milk™ Reparative Leave-In Conditioning Spray Mini']
    self.df_prod_pages=self.df_prod_pages[~self.df_prod_pages.displayName.isin(rosarco_milk_list)]


  def binarize_oos(self):
    self.df_prod_pages['OOS_FewLeft_binary']=self.df_prod_pages['OOS_FewLeft'].apply(lambda x: 0 if x in ['No'] else 1)

  def save_df_prod_pages(self):
    self.df_prod_pages.to_excel('oos_files/df_prod_pages_{}.xlsx'.format(datetime.now().date()),index=False)


  def parse_all_products(self):
    #print('Removing Rosarco™ Blow Dry Perfection Heat Protectant Crème from product list.')
    #self.df_prod_pages=self.df_prod_pages[~self.df_prod_pages.displayName.isin(['Rosarco Blow Dry Perfection & Heat Protectant Crème','Rosarco™ Blow Dry Perfection Heat Protectant Crème','Rosarco Blow Dry Perfection Heat Protectant Crème - Crème Cheveux Protectrice','Rosarco™ Blow Dry Perfection & Heat Protectant Crème'])]
    self.remove_products()
    r_list=list(self.df_prod_pages['Retailer'].unique())
    for r in r_list:
      self.parse_retailer_products(r)
    #self.df_prod_pages['OOS_FewLeft']=self.df_prod_pages.apply(lambda x: self.parse_product_page(x['Retailer'],x['targetUrl'],x['OOS_FewLeft']),axis=1)
    self.binarize_oos()
    #self.df_prod_pages['OOS_FewLeft_binary']=self.df_prod_pages['OOS_FewLeft'].apply(lambda x: 0 if x in ['No'] else 1)
    self.save_df_prod_pages()
    #self.df_prod_pages.to_excel('oos_files/df_prod_pages_{}.xlsx'.format(datetime.now().date()),index=False)

  def parse_all_products_random(self):
    self.df_prod_pages=self.df_prod_pages.sample(frac=1).reset_index(drop=True)
    for p in range(len(self.df_prod_pages)):
      try:
        oos_value=self.df_prod_pages[self.df_prod_pages['targetUrl']==self.df_prod_pages.loc[p]['targetUrl']].apply(lambda x: self.parse_product_page(x['Retailer'],x['targetUrl'],x['OOS_FewLeft']),axis=1)
      except:
        oos_value='Fail'
      self.df_prod_pages.loc[self.df_prod_pages['targetUrl']==self.df_prod_pages.loc[p]['targetUrl'],'OOS_FewLeft']=oos_value

  def parse_retailer_products(self,retailer):
    self.df_prod_pages.loc[self.df_prod_pages['Retailer']==retailer,'OOS_FewLeft']=self.df_prod_pages[self.df_prod_pages['Retailer']==retailer].apply(lambda x: self.parse_product_page(x['Retailer'],x['targetUrl'],x['OOS_FewLeft']),axis=1)

  def parse_product_page(self,retailer,product_url,oos_value):
    ### SEPHORA USA AND SEPHORA CANADA 
    if retailer in ['Sephora USA','Sephora CAN']:
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_requests(product_url)
      time.sleep(2)
      data = self.soup.find('script',attrs={'id':"linkJSON"}).get_text()
      output = json.loads(data)
      for d in output:
        if d['path']=='RegularProductTop':
          prod=d['props']['currentProduct']
          if 'regularChildSkus' in prod.keys():
            field='regularChildSkus'
            for sku in prod[field]:
              print(sku['targetUrl'], sku['skuName'], ' OOS:', sku['isOutOfStock'], ' FewLeft:', sku['isOnlyFewLeft'])
              if sku['isOutOfStock']:
                oos_value='OOS'
                #text_file.write("\nOOS: {0} {1}\n".format(urlroot+sku['targetUrl'], sku['skuName']))
              if sku['isOnlyFewLeft']:
                oos_value='Few Left'
                #text_file.write("\mFEW_LEFT: {0} {1}\n".format(urlroot+sku['targetUrl'], sku['skuName']))
          else:
            field='currentSku'
            sku=prod[field]
            print(sku['targetUrl'], ' OOS:', sku['isOutOfStock'], ' FewLeft:', sku['isOnlyFewLeft'])
            if sku['isOutOfStock']:
              oos_value='OOS'
              #  text_file.write("\nOOS: {0}\n".format(urlroot+sku['targetUrl']))
            if sku['isOnlyFewLeft']:
              oos_value='Few Left'
              #  text_file.write("\nFEW_LEFT: {0}\n".format(urlroot+sku['targetUrl']))
    ### SEPHORA FRANCE
    elif retailer == 'Sephora France':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      #self.load_page_requests(product_url)
    ### SEPHORA MIDDLE EAST
    elif retailer in ['Sephora Middle East']:
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_requests(product_url)
      if self.soup.find('div',attrs={'class':'out-of-stock'}):
        oos_value='OOS'
      else:
        oos_value='No'
    ### SEPHORA SOUTH EAST ASIA
    ### SEPHORA THAILAND
    ### SEPHORA AUSTRALIA
    elif retailer in ['Sephora SE Asia','Sephora Thailand','Sephora AUS']:
      print('{}: Not loading any pages. OOS information from brand page.'.format(retailer))
    ### NORDSTROM
    elif retailer == 'Nordstrom':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_requests(product_url)
      time.sleep(1+np.abs(np.random.rand()))
      nd_prod_start_pos=self.soup.text.find('__INITIAL_CONFIG__ = {')
      #nd_prod_end_pos=self.soup.text.find('}}\n[]\n\n\n',nd_prod_start_pos)
      #nd_prod_jsondata=json.loads(self.soup.text[nd_prod_start_pos+21:nd_prod_end_pos+2])
      nd_prod_end_pos=self.soup.text.find('webExtractor":{}}',nd_prod_start_pos)
      nd_prod_jsondata=json.loads(self.soup.text[nd_prod_start_pos+21:nd_prod_end_pos+17])
      for k in nd_prod_jsondata['stylesById']['data']:
        prod_name=nd_prod_jsondata['stylesById']['data'][k]['productTitle']
        oos_value=nd_prod_jsondata['stylesById']['data'][k]['price']['style']['showSoldOutMessage']
      if oos_value==True:
        oos_value='OOS'
      else:
        oos_value='No'
    ### RILEY ROSE
    elif retailer == 'Riley Rose':
      print('{}: Not loading any pages. OOS information from brand page.'.format(retailer))
    ### REVOLVE
    elif retailer == 'Revolve':
      print('{}: Not loading any pages. OOS information from brand page.'.format(retailer))
    ### BIRCHBOX
    elif retailer == 'Birchbox':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_selenium(product_url,By.CLASS_NAME,"productCard__descriptionsWide___1Ib8D",scroll=False,click=False)
      time.sleep(5)
      butts=self.soup.find_all('button')
      oos_flag=False
      for b in butts:
        if b.text == 'Join Waitlist':
          oos_flag=True
      if oos_flag:
        oos_value='OOS'
      else:
        oos_value='No'
    ### NET-A-PORTER
    elif retailer == 'Net-A-Porter':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_selenium(product_url,By.CLASS_NAME,"container-details",scroll=False,click=False)
      if self.soup.find('div',attrs={'id':'sold-out-container','class':'sold-out-container'}):
        oos_value='OOS'
      else:
        oos_value='No'
    ### BEAUTY BAY
    elif retailer == 'Beauty Bay':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_selenium(product_url,By.CLASS_NAME,"product-description",scroll=False,click=False)
      time.sleep(12)
      if self.soup.find('button',attrs={'class':"quantity-selector__btn btn action btn-add-bag js-track-add "}):
        oos_value='No'
      else:
        oos_value='OOS'
    ### CULT BEAUTY
    elif retailer == 'Cult Beauty':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_selenium(product_url,By.CLASS_NAME,"productHeaderContainer",scroll=False,click=False)
      variants=self.soup.find('div',attrs={'class','productAlterationsContainer'})['data-variant-ids'].split(',')
      if len(variants)>1:
        oos_flag=0
        for v in variants:
          click_link=self.driver.find_element_by_xpath("//li[@data-variant-id={}]".format(v))
          click_link.click()
          html = self.driver.execute_script("return document.body.outerHTML;")
          self.soup=BeautifulSoup(html,'lxml')
          if self.soup.find('button',attrs={'class':"btn addCartButton js-add-to-cart"})['style']=='display: inline-block;':
            if oos_flag==1:
              oos_value=oos_value
            else:
              oos_value='No'
          else:
            oos_flag+=1
            p_size=self.soup.find('li',attrs={'data-variant-id':v})['data-option-value']
            if oos_flag==1:
              oos_value='OOS '+p_size
            else:
              oos_value+=', '+p_size
      else:
        if self.soup.find('button',attrs={'class':"btn addCartButton js-add-to-cart"})['style']=='display: inline-block;':
          oos_value='No'
        else:
          oos_value='OOS'
    ### ANTHROPOLOGIE
    elif retailer == 'Anthropologie':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_selenium(product_url,By.CLASS_NAME,"dom-product-bopis",scroll=False,click=False)
      time.sleep(10)
      if self.soup.find('p',attrs={'class':'c-product-message__sold-out'}):  
        oos_value='OOS'
      else:
        is_limited=self.soup.find('div',attrs={'class':'dom-product-bopis'}).find('p',attrs={'class':'c-product-bopis__p--warning'})
        if is_limited:
          oos_value='LQA {}'.format(is_limited['data-qa-product-msg-warning'])
        else:
          oos_value='No'
    ### FREE PEOPLE
    elif retailer == 'Free People':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      #self.load_page_requests(product_url)
      self.load_page_selenium(product_url,By.CLASS_NAME,"c-product-container__sku-controls",scroll=False,click=False)
      time.sleep(1+np.abs(np.random.rand()))
      add_to_bag_div=self.soup.find('div',attrs={'class':'dom-add-to-cart'})
      if add_to_bag_div:
        oos_value='No'
      else:
        oos_value='OOS'
    ### I AM NATURAL STORE
    elif retailer == 'I Am Natural Store':
      print('{}: Not loading any pages. OOS information from brand page.'.format(retailer))
    ### URBAN OUTFITTERS
    elif retailer == 'Urban Outfitters':
      print('{}: Loading product page: {}'.format(retailer,product_url))
      self.load_page_selenium(product_url,By.CLASS_NAME,"js-product-meta",scroll=False,click=False)
      if self.soup.find('button',attrs={'class':"js-add-to-cart"}):
        if self.soup.find('p',attrs={'class':'c-product-bopis__p--warning'}):
          oos_value='Few Left'
        else:
          oos_value='No'
      else:
        oos_value='OOS'
    ### NATURISMO
    elif retailer == 'Naturisimo':    
      print('{}: Not loading any pages. OOS information from brand page.'.format(retailer))


    return oos_value


  
  def compose_oos_email(self,dont_send=False,send_to='btquinn@gmail.com'):
    subject = 'Briogeo Out of Stock Report for the Date: {}'.format(datetime.now().date())
    text = '<html><head><style>{}</style></head><body>\n'.format(utils.CSS)
    text += '<table>\n'
    text += '<tr><th>Retailer</th><th>Product OOS</th></tr>\n'
    n_retailers = len(self.df_prod_pages['Retailer'].unique())
    df_oos = self.df_prod_pages[self.df_prod_pages['OOS_FewLeft']!='No']
    oos_rtlr_list = list(df_oos['Retailer'].unique())
  
    for r in oos_rtlr_list:
      df_rtlr_oos = df_oos[df_oos['Retailer']==r]
      text += '<tr><td align="center">{}</td>\n<td>'.format(r)
      count=0
      for index, row in df_rtlr_oos.iterrows():
        if count>0:
          text += '\n<br/>'
        text += ('<a href={}>[{}]: {}</a>\n').format(row['targetUrl'],row['OOS_FewLeft'],row['displayName'])
        count+=1
      text += '</td></tr>\n'

    text += '</table>\n'

    text += '<p>The following {} retailers were included in this report:<br>\n'.format(n_retailers)
    
    table_df=self.df_prod_pages[['Retailer','OOS_FewLeft_binary']].groupby(['Retailer'],sort=False).agg({'OOS_FewLeft_binary':['count', 'sum',lambda x: (x.sum()/x.count()*100).round(2)]}).rename(index=str,columns={'count':'total products','sum':'OOS','<lambda>':'% OOS'})
    table_df.columns = table_df.columns.get_level_values(-1)
    text += table_df.reset_index().to_html(index=False)
    
    text += '</body>\n<html>\n'
    self.email_text = text
    if dont_send == False:
      #mail.send_email('briogeods@gmail.com', subject, text, to='orders@briogeohair.com')
      mail.send_email('briogeods@gmail.com', subject, text, to=send_to)



  def quit(self):
    if not self.driver:
      pass
    else:
      try: 
        self.driver.close()
      except ConnectionResetError:
        print('ConnectionResetError 726')
        self.driver.close()
      except BrokenPipeError:
        print('BrokenPipeError 729')
        self.driver.close()


if __name__ == '__main__':
  scraper = BriogeoRetailerScraper()
  scraper.load_and_parse_all_brand_pages()
  scraper.parse_all_products()
  scraper.compose_oos_email(send_to='orders@briogeohair.com,sales@briogeohair.com')
  scraper.quit()
  exit()


