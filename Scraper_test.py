
# coding: utf-8

# In[1]:


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


# In[2]:


##   "Sephora USA": f"http://www.sephora.com/brand/briogeo/all"
##  ,"Sephora CAN": f"http://www.sephora.com/ca/en/brand/briogeo/all"
##  ,"Sephora France": f"http://www.sephora.fr/marques/de-a-a-z/briogeo-briog/"
##  ,"Sephora Middle East": f"http://www.sephora.ae/en/brands/briogeo"
##  ,"Sephora SE Asia": f"http://www.sephora.sg/brands/briogeo?view=120"
##  ,"Sephora Thailand": f"http://www.sephora.co.th/brands/briogeo?view=120"
##  ,"Sephora AUS": f"https://www.sephora.com.au/brands/briogeo?view=60"
##  ,"Revolve": f"http://www.revolve.com/briogeo/br/2e2c0b/"
##  ,"Riley Rose": f"https://www.rileyrose.com/us/shop/catalog/category/rr/promo-branded-briogeo"
##  ,"Birchbox": f"http://www.birchbox.com/brand/4614"
##  ,"Nordstrom": f"https://shop.nordstrom.com/c/briogeo?origin=productBrandLink"
##  ,"Net-A-Porter": f"https://www.net-a-porter.com/us/en/Shop/Designers/Briogeo?pn=1&npp=60&image_view=product&dScroll=0"
##  ,"Beauty Bay": f"https://www.beautybay.com/l/briogeo/"
##  ,"Cult Beauty": f"https://www.cultbeauty.co.uk/briogeo"
##  ,"Anthropologie": f"https://www.anthropologie.com/beauty-hair-care?brand=Briogeo"
##  ,"Free People": f"https://www.freepeople.com/brands/briogeo/"
##  ,"I Am Natural Store": f"https://www.iamnaturalstore.com.au/collections/briogeo"
##  ,"Urban Outfitters": f"https://www.urbanoutfitters.com/brands/briogeo"
##  ,"Naturismo": f"https://www.naturisimo.com/index.cfm?nme=bri"

##  ,"B-Glowing": f"https://www.b-glowing.com/briogeo/?limit=99"
##  ,"Naturally Curly": f"https://shop.naturallycurly.com/brands/Briogeo.html"
##  ,"Naturally Curly ": f"https://shop.naturallycurly.com/brands/Briogeo.html?sort=featured&page=2"
##  ,"Niche Beauty": f"https://www.niche-beauty.com/en-de/brands/briogeo-709"
##  ,"Skin Store": f"https://www.skinstore.com/hair-care/see-all-hair-care.list?facetFilters=en_brand_content:Briogeo"

## BOT DETECTION! url=f"https://www.feelunique.com/brands/briogeo" # FEELUNIQUE 
## BOT DETECTION! url=f"https://www.dermstore.com/profile_Briogeo_502970.htm" #DERMSTORE
## BOT DETECTION! bloomingdales

##  costco



# ## Anthropologie

# In[10]:


url=f"https://www.anthropologie.com/beauty-hair-care?brand=Briogeo"

driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"dom-category-browse"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
    


# In[6]:


prods=soup.find_all('a',attrs={'class':'c-product-tile__image-link js-product-tile__image-link'})


# In[7]:


#prods=soup.find_all('a',attrs={'class':'c-product-tile__image-link'})
print(len(prods))


# In[8]:


for p in prods:
  print('https://www.anthropologie.com'+p['href'])
  img=p.find('img')
  print(img['alt'])


# In[11]:


url='https://www.anthropologie.com/shop/briogeo-rosarco-oil?category=beauty-hair-care&color=010'

driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"dom-product-bopis"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
    


# In[13]:


is_soup=soup


# In[14]:


is_soup.find('div',attrs={'class':'dom-product-bopis'})


# In[26]:


is_limited=is_soup.find('div',attrs={'class':'dom-product-bopis'}).find('p',attrs={'class':'c-product-bopis__p--warning'})
is_limited


# In[15]:


url='https://www.anthropologie.com/shop/briogeo-dont-despair-repair-deep-conditioning-mask?category=beauty-hair-care&color=010'

driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"dom-product-bopis"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
    


# In[16]:


oos_soup=soup


# In[17]:


oos_soup.find('div',attrs={'class':'dom-product-bopis'})


# In[29]:


is_limited=oos_soup.find('div',attrs={'class':'dom-product-bopis'}).find('p',attrs={'class':'c-product-bopis__p--warning'})
if is_limited:
    print(is_limited['data-qa-product-msg-warning'])


# In[21]:


url='https://www.anthropologie.com/shop/briogeo-dont-despair-repair-strength-moisture-leave-in-mask-spray?category=beauty-hair-care&color=010'

driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"dom-product-bopis"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
    


# In[22]:


oos_nod_soup=soup


# In[23]:


oos_nod_soup.find('div',attrs={'class':'dom-product-bopis'})


# In[30]:


is_limited=oos_nod_soup.find('div',attrs={'class':'dom-product-bopis'}).find('p',attrs={'class':'c-product-bopis__p--warning'})
if is_limited:
    print(is_limited['data-qa-product-msg-warning'])


# ## Cult Beauty

# In[86]:


url=f"https://www.cultbeauty.co.uk/briogeo"
html_page=requests.get(url,verify=False)
soup=BeautifulSoup(html_page.content,'lxml')


# In[88]:


prods=soup.find_all('div',attrs={'class':'productGridItem'})
for p in prods:
    long_url=p.find('a')['href']
    end_url_loc=long_url.find('.html#')
    url=long_url[0:end_url_loc+5]
    name=p['data-name']
    print(name,url)


# In[126]:


#url=f"https://www.cultbeauty.co.uk/briogeo-hair-o-scopes.html" #OOS
url=f"https://www.cultbeauty.co.uk/briogeo-don-t-despair-repair-super-moisture-shampoo.html" #inStock
html_page=requests.get(url,verify=False)
soup=BeautifulSoup(html_page.content,'lxml')


# In[ ]:


#out of stock div:
#<div class="exclHeader exclHeader--stockSoon">In Stock Soon!</div>
<div class="exclWidgetWrapper js-excl-widget-wrapper">

#in stock div:
<div class="exclWidgetWrapper js-excl-widget-wrapper hidden">
               


# In[112]:


print(soup.find('div',attrs={'class':"exclWidgetWrapper js-excl-widget-wrapper"}))


# In[113]:


print(soup.find('div',attrs={'class':"exclWidgetWrapper js-excl-widget-wrapper hidden"}))


# In[111]:


print(soup.find('div',attrs={'class':'productActionsContainer js-product-actions-toolbar'}))


# In[114]:


print(soup)


# In[128]:


url=f"https://www.cultbeauty.co.uk/briogeo-hair-o-scopes.html" #OOS
url=f"https://www.cultbeauty.co.uk/briogeo-don-t-despair-repair-super-moisture-shampoo.html"

driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"productHeaderContainer"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
    


# In[118]:


print(soup.find('div',attrs={'class':"exclWidgetWrapper js-excl-widget-wrapper"}))


# In[129]:


print(soup.find('button',attrs={'class':"btn addCartButton js-add-to-cart"})['style'])


# In[116]:


print(soup.find('div',attrs={'class':'productActionsContainer js-product-actions-toolbar'}))


# In[119]:


print(soup)


# ## Beauty Bay

# In[58]:


url=f"https://www.beautybay.com/l/briogeo/"
driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"o-lister"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
    


# In[67]:


prods=soup.find_all('a',attrs={'class':'c-product qa-product'})
print(len(prods))
for p in prods:
    print(p['href'],p.find('img')['alt'])


# In[66]:


p.find('img')['alt']


# In[68]:


url=f"https://www.beautybay.com/p/briogeo/scalp-revival-charcoal-tea-tree-scalp-treatment/"
driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"product-description"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
    


# In[83]:


print(soup.find('button',attrs={'class':"quantity-selector__btn btn action btn-add-bag js-track-add "}).string)


# In[74]:


print(soup.find('div',attrs={'id':'add-to-bag'}).prettify())


# ## Feelunique -- BOT DETECTION

# In[57]:


url=f"https://www.feelunique.com/brands/briogeo?all=1&filter=fh_location=//c1/en_GB/brand%3d%7ba1594%7d/!exclude_countries%3Eus/!site_exclude%3E1%26fh_view_size=36"
driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.ID,"rightcolumn"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = self.driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')


# ## Net-A-Porter

# In[53]:


url=f'https://www.net-a-porter.com/us/en/Shop/Designers/Briogeo?pn=1&npp=60&image_view=product&dScroll=0'
driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.ID,"page-container"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = self.driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')


# In[ ]:


prod_list=soup.find_all('div',attrs={'class':'product-image'})
prod_name_list=[]
prod_url_list=[]
for p in prod_list:
    prod_name_list.append(p.find('a').find('img')['alt'])
    prod_url_list.append(retailer_urls_all[retailer]+p.find('a')['href'])


# In[56]:


url=f'https://www.net-a-porter.com/product/1125351/Briogeo/rosarco-repair-shampoo-240ml'
driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10
driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.CLASS,"container-details"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")

scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

html = self.driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')


# # BirchBox

# In[48]:


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


# In[41]:





# In[51]:


scroll_height=driver.execute_script("return document.body.scrollHeight;")
print(scroll_height)
scroll_to=300
loop_limit=30
loop_cnt=1
while scroll_to < scroll_height:
    if loop_cnt>loop_limit:
        break
    print(scroll_to,scroll_height)
    driver.execute_script("window.scrollTo(0, {});".format(scroll_to))
    time.sleep(1+np.abs(np.random.rand()))
    scroll_height=driver.execute_script("return document.body.scrollHeight;")
    scroll_to+=300
    loop_cnt+=1

print(scroll_to,scroll_height)

#for scroll_to in range(10,scroll_height,200):
#    driver.execute_script("window.scrollTo(0, {});".format(x))
#    time.sleep(1+np.abs(np.random.rand()))
#    new_sh=driver.execute_script("return document.body.scrollHeight;")
#    print(x,new_sh)


# In[5]:


k=2
"window {0}".format(k)
import numpy as np


# In[6]:


np.random.rand()


# In[26]:


driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# In[36]:


#continue_link = driver.find_element_by_link_text('Load More Products')
continue_link = driver.find_element_by_xpath("//button[1]")


# In[38]:


continue_link.click()


# In[32]:


import sys
import time
sys.stdout.flush()
#try:
#window.scrollTo(0, document.body.scrollHeight)
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

#driver.find_element_by_class_name
test=driver.find_elements_by_partial_link_text('Briogeo')

print(len(test))

html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
print(soup.contents)


# In[10]:


print(len(soup.find_all('a',attrs={'class':'productThumb__title___1D-Rj'})))
prod_thumb=soup.find_all('a',attrs={'class':'productThumb__title___1D-Rj'})
for this_one in prod_thumb:
  #this_one=prod_thumb[0]
  print(this_one.attrs['href'])
  print(this_one.text)
base_url='https://www.birchbox.com/'


# In[11]:


bb_oos_page_url='https://www.birchbox.com/product/25768'
bb_oos_page=requests.get(bb_oos_page_url)
bb_oos_soup=BeautifulSoup(bb_oos_page.content,'lxml')


# In[104]:


bb_oos_page_url='https://www.birchbox.com/product/25768'
bb_is_page_url='https://www.birchbox.com/product/25565'

#bb_oos_page=requests.get(bb_oos_page_url)
#bb_oos_soup=BeautifulSoup(bb_oos_page.content,'lxml')
driver.get(bb_oos_page_url)
try:
  wait=WebDriverWait(driver,delay)
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"newProductCard_price__m3Jaa"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")
bb_oos_html = driver.execute_script("return document.body.outerHTML;")
bb_oos_soup=BeautifulSoup(bb_oos_html,'lxml')
print(bb_oos_soup.contents)

driver.get(bb_is_page_url)
try:
  wait=WebDriverWait(driver,delay)
  wait.until(EC.presence_of_element_located((By.CLASS_NAME,"newProductCard_price__m3Jaa"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")
bb_is_html = driver.execute_script("return document.body.outerHTML;")
bb_is_soup=BeautifulSoup(bb_is_html,'lxml')
print(bb_is_soup.contents)
#bb_is_page=requests.get(bb_is_page_url)
#bb_is_soup=BeautifulSoup(bb_is_page.content,'lxml')


# In[102]:


print(bb_oos_soup.contents)


# ## Sephora Thailand

# In[4]:


url=f"http://www.sephora.co.th/brands/briogeo?view=120"
driver=webdriver.Firefox()
#driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
delay=10

driver.get(url)
try:
  wait=WebDriverWait(driver,delay)
  # DERMSTORE wait.until(EC.presence_of_element_located((By.ID,"tab_products")))
  wait.until(EC.presence_of_element_located((By.ID,"product-index-content"))) #BIRCHBOX
  print("page is ready")
except TimeoutException:
  print("Loading took too much time")


# In[6]:


html = driver.execute_script("return document.body.outerHTML;")
soup=BeautifulSoup(html,'lxml')
print(soup.contents)


# In[11]:


prod_ind=soup.find('div',attrs={'class':'products-grid'})
print(prod_ind.prettify())


# In[19]:


prods=prod_ind.find_all('div',attrs={'class':'product-card'})
print(prods[-1].prettify())


# In[20]:


print(prods[0].prettify())


# In[21]:


#prods=prod_ind.find_all('a',attrs={'class':'product-card-description'})
len(prods)


# In[24]:


prod_name_list=[]
prod_url_list=[]
prod_oos_list=[]
for p in prods:
    print(p.find('p',attrs={'class':'product-card-product'}).text)
    print(p.find('a',attrs={'class':'product-card-description'})['href'])
    if p.find('div',attrs={'class':'out-of-stock'}):
        print('OOS')
    else:
        print('inStock')


# In[38]:


print(type(driver))
if not driver:
    print('not defined')


# # Nordstrom

# In[7]:


import requests
this_url=f"https://shop.nordstrom.com/c/briogeo?origin=productBrandLink" #NORDSTROM 
html_page=requests.get(this_url)
nordsoup=BeautifulSoup(html_page.content,'lxml')


# In[8]:


print(nordsoup.text)


# In[9]:


nd_start_pos=nordsoup.text.find('{renderer({')
nd_end_pos=nordsoup.text.find('});',nd_start_pos)
print(nd_start_pos, nd_end_pos)


# In[10]:


print(nordsoup.text[nd_start_pos+10:nd_end_pos+1])


# In[13]:


import json
nd_jsondata = json.loads(nordsoup.text[nd_start_pos+10:nd_end_pos+1])


# In[14]:


for k in nd_jsondata.keys():
    print(k)


# In[15]:


nd_jsondata['viewData']['productsById']


# In[16]:


product_pages=[]
for num,p in enumerate(nd_jsondata['viewData']['productsById'].keys(),1):
    print(num, nd_jsondata['viewData']['productsById'][p]['name'])
    print('https://nordstrom.com/'+nd_jsondata['viewData']['productsById'][p]['productPageUrl'])
    product_pages.append('https://nordstrom.com/'+nd_jsondata['viewData']['productsById'][p]['productPageUrl'])


# In[17]:


nd_prod_html_page=requests.get(product_pages[0])
nordprodsoup=BeautifulSoup(nd_prod_html_page.content,'lxml')


# In[18]:


print(nordprodsoup.text)


# ### Possible flags to indicate OOS status
# "isPreOrder":false
# 
# "isAvailable":true
# 
# "isBackOrder":false

# In[19]:


nd_prod_start_pos=nordprodsoup.text.find('{renderer({')
nd_prod_end_pos=nordprodsoup.text.find('});',nd_prod_start_pos)
print(nd_prod_start_pos, nd_prod_end_pos)


# In[20]:


nd_prod_jsondata = json.loads(nordprodsoup.text[nd_prod_start_pos+10:nd_prod_end_pos+1])


# In[21]:


for k in nd_prod_jsondata.keys():
    print(k)


# In[22]:


for k in nd_prod_jsondata['stylesById']['data'].keys():
    


# In[179]:


print(nd_prod_jsondata['stylesById']['data'].keys())


# In[23]:


print(nd_prod_jsondata['stylesById']['data']['4873076']['productTitle'])
print(nd_prod_jsondata['stylesById']['data']['4873076']['isPreOrder'])
print(nd_prod_jsondata['stylesById']['data']['4873076']['isAvailable'])
print(nd_prod_jsondata['stylesById']['data']['4873076']['price']['style']['showSoldOutMessage'])


# In[158]:


print(nordsoup.contents)


# # Riley Rose

# In[24]:


import requests
rr_url=f"https://www.rileyrose.com/us/shop/catalog/category/rr/promo-branded-briogeo"
rr_html_page=requests.get(rr_url)
rr_soup=BeautifulSoup(rr_html_page.content,'lxml')


# In[25]:


print(rr_soup.contents)


# In[26]:


rr_scripts=rr_soup.find_all('script',attrs={'type':'text/javascript'})


# In[27]:


for sc in rr_scripts:
    print(sc.attrs)


# In[28]:


start_pos=rr_scripts[-1].text.find('var cData =')
end_pos=rr_scripts[-1].text.find('"};',start_pos)
print(rr_scripts[-1].text[start_pos+12:end_pos+2])


# In[29]:


import json
jsondata = json.loads(rr_scripts[-1].text[start_pos+12:end_pos+2])


# In[30]:


for k in jsondata.keys():
    print(k)


# In[31]:


print(jsondata['TotalRecords'])


# In[32]:


print(jsondata['CatalogProducts'][0].keys())


# In[34]:


jsondata['CatalogProducts'][0]


# In[38]:


jsondata['CatalogProducts'][1]


# In[50]:


jsondata['CatalogProducts'][6]


# In[33]:


for p in jsondata['CatalogProducts']:
  print(p['DisplayName'], p['IsOOS'])    
  #print(jsondata['CatalogProducts'][0]['DisplayName'], jsondata['CatalogProducts'][0]['IsOOS'])


# In[121]:


'alc'.find('l',2)


# In[61]:


souper=BeautifulSoup(html_page.content,'lxml')


# In[74]:


for t in test:
    print(t.text)


# In[ ]:


html = driver.execute_script("return document.body.innerHTML;")
soup=BeautifulSoup(html,'lxml')
print(soup.text)


# In[23]:


# For Birchbox, need to scroll slowly to load all the products
SCROLL_PAUSE_TIME = 0.6
import time

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# ## Sephora

# In[3]:


import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

import urllib3
urllib3.disable_warnings()


# In[18]:


brand_page='https://www.sephora.com/brand/briogeo/all'
resp=requests.get(brand_page,verify=False)
soup = BeautifulSoup(resp.content,"lxml")


# In[5]:


print(soup.contents)


# In[19]:


prods=soup.find_all('a',attrs={'data-comp':"ProductItem"})
print(len(prods))


# In[17]:


for p in prods:
    print(p['href'].split('?')[0])

