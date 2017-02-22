
# coding: utf-8

# In[1]:

import time
import urllib2
import requests
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from IPython.display import IFrame
import matplotlib.font_manager as fm

plt.style.use('ggplot')
get_ipython().magic(u'matplotlib inline')
pd.options.display.max_columns=25


# In[47]:

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
    print 'Parsing' + url
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
    if p==1:
        page_df['rank']=page_df.index+1
        seph_df = page_df
    else:
        page_df['rank']=page_df.index+seph_df.shape[0]+1
        seph_df = pd.concat([seph_df,page_df])

seph_df['pct_rank']=seph_df['rank'].div(seph_df.shape[0]).mul(100)
#Reorder columns
seph_df = seph_df[['date_scraped','rank','pct_rank','brand_name','display_name','rating','id','product_url']]

filename_out = 'sephora_hair_search_' + str(datetime.now().date()) + '.xlsx'
seph_df.to_excel(filename_out,index=False)
filename_out2 = 'briogeo_sephora_hair_search_' + str(datetime.now().date()) + '.xlsx'
seph_df[seph_df['brand_name']=='Briogeo'].to_excel(filename_out2,index=False)


# In[8]:

print response.content
soup = BeautifulSoup(response.content,"lxml")


# In[34]:

data = soup.find('script',attrs={'id':"searchResult"}).get_text()
output = json.loads(data)
#print output
print output['products'].viewkeys()
#pd.read_json(output['products']['products'],orient='records')
df=pd.DataFrame(output['products']['products'])


# In[37]:

df['rank']=df.index+1
df['date_scraped']=datetime.now()
df = df[['date_scraped','rank','brand_name','display_name','rating','id','product_url']]
df.head()


# In[39]:

df['brand_name'].unique()


# In[40]:

df[df['brand_name']=='Briogeo']


# In[42]:

print df.shape
df


# In[24]:

output['products'].viewkeys()


# In[6]:

import json, urllib
data = urllib.urlopen(url).read()
output = json.loads(data)
print (output)


# In[3]:

urlroot = 'http://www.sephora.com/search/search.jsp?keyword=hair&mode=all&node=1050092&sortBy=P_BEST_SELLING%3A1%3A%3AP_RATING%3A1%3A%3AP_PROD_NAME%3A0%3A%3AP_DEFAULT_SKU%3A1&pageSize=-1'
pnum=1
productlinklist = [] 
url = urlroot+'?currentPage='+str(pnum)
print 'Parsing '+url


# In[7]:

resp2 = requests.get(urlroot)


# In[ ]:

import mechanize
br = mechanize.Browser()
import cookielib
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
data = br.open(resp2.url).get_data()


# In[ ]:

print data


# In[10]:

soup = BeautifulSoup(data,"lxml")
#soup.
'''
<a ng-href="/supersonic-hair-dryer-P410214?skuId=1870179&amp;icid2=products grid:p410214" class="u-size1of4 SkuItem SkuItem--135 SkuItem SkuItem--135" data-at="sku_item_1870179" seph-sku-item="" ana-click-thru="" ng-repeat="sku in skugroup.sku_list" href="/supersonic-hair-dryer-P410214?skuId=1870179&amp;icid2=products grid:p410214">
  <div>
    <div class="has-ql u-mxa" ng-style="::{'max-width': imageSize}" style="max-width: 135px;">
      <div class="FlexEmbed">
        <div class="FlexEmbed-ratio"></div>
        <img class="FlexEmbed-content" data-lazyload="" seph-lazy-src="/productimages/sku/s1870179-main-grid.jpg" src="/productimages/sku/s1870179-main-grid.jpg">
      </div>
      <!-- ngIf: ::sku.is_beauty_insider -->
      <!-- ngIf: ::!skugroup.hideQuickLook --><span ng-if="::!skugroup.hideQuickLook" seph-quick-look="" data-product-id="P410214" data-sku_number="1870179" class="ShowQL ng-scope" data-at="ql_show" ana-event-info="{&quot;clickOrigin&quot;:{&quot;componentSubType&quot;: &quot;&quot;}}">Quick Look</span><!-- end ngIf: ::!skugroup.hideQuickLook -->
    </div>
  </div>
  <div class="SkuItem-newLove">
    <!-- ngIf: ::sku.is_new -->
    <!-- ngIf: ::(skugroup.is_loves_shown && sku.isLoveEligible()) --><div class="SkuItem-love ng-scope" ng-if="::(skugroup.is_loves_shown &amp;&amp; sku.isLoveEligible())">
      <button type="button" seph-tooltip="" uib-tooltip-html="loveTooltip" tooltip-append-to-body="true" class="LoveIcon is-hoverable" seph-lovable="P410214" ng-class="{'is-loved': isLoved, 'is-hoverable': hoverEnable}" data-sku_number="1870179" data-at="sku_item_love"><svg class="Icon Icon--love"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-love"></use></svg>
<svg class="Icon Icon--loveOutline"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-loveOutline"></use></svg>
<svg class="Icon Icon--loveHover"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-loveHover"></use></svg>
</button>
    </div><!-- end ngIf: ::(skugroup.is_loves_shown && sku.isLoveEligible()) -->
  </div>
  <div class="SkuItem-info">
    <!-- ngIf: ::skugroup.is_numbers_shown -->
    <div class="SkuItem-name">
      <div class="SkuItem-nameBrand OneLinkNoTx ng-binding" data-at="sku_item_brand" ng-bind-html="trust(sku.primary_product.brand_name)">dyson</div>
      <div class="SkuItem-nameDisplay ng-binding" data-at="sku_item_name" ng-bind-html="trust(sku.primary_product.display_name)">Supersonic Hair Dryer</div>
    </div>
    <!-- ngIf: ::skugroup.is_price_shown!==false --><div class="u-fwb ng-scope" ng-if="::skugroup.is_price_shown!==false">
      <span data-at="sku_item_price_list" ng-class="::{'u-fwn u-strike u-midGray': sku.sale_price || sku.sale_price_min}" class="ng-binding">$399.00</span>
      <!-- ngIf: ::sku.sale_price -->
      <!-- ngIf: ::sku.sale_price_min -->
      <!-- ngIf: ::sku.value_price -->
    </div><!-- end ngIf: ::skugroup.is_price_shown!==false -->
    <!-- ngIf: ::skugroup.flags --><div class="SkuItem-flags u-mt1 u-mb1 ng-scope" data-at="sku_item_flags" ng-if="::skugroup.flags">
      <!-- ngIf: ::sku.is_sephora_exclusive -->
      <!-- ngIf: ::sku.is_limited_edition -->
      <!-- ngIf: ::sku.is_online_only -->
    </div><!-- end ngIf: ::skugroup.flags -->
    <!-- ngIf: ::(sku.primary_product.more_colors && !sku.primary_product.isNoShowMore()) --><div ng-if="::(sku.primary_product.more_colors &amp;&amp; !sku.primary_product.isNoShowMore())" class="SkuItem-colors u-mt2 u-mb2 ng-binding ng-scope">
      [ 1 more <span ng-pluralize="" count="::sku.primary_product.more_colors" when="{'one': 'color', 'other': 'colors'}">color</span> ]
    </div><!-- end ngIf: ::(sku.primary_product.more_colors && !sku.primary_product.isNoShowMore()) -->
    <!-- ngIf: ::(skugroup.is_rating_shown && !sku.primary_product.is_hide_social) --><div class="u-db u-mxa u-mt2 u-mb2 StarRating u-relative u-oh ng-scope" ng-if="::(skugroup.is_rating_shown &amp;&amp; !sku.primary_product.is_hide_social)" seph-stars="4.3735">
  <div class="StarRating-set u-moonGray">
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
  </div>
  <div class="StarRating-set u-absolute u-top0 u-left0 u-oh u-red" ng-style="{'width': rating+'%'}">
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
    <svg class="Icon Icon--star"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/images/icon.svg#icon-star"></use></svg>
  </div>
</div><!-- end ngIf: ::(skugroup.is_rating_shown && !sku.primary_product.is_hide_social) -->
  </div>
  <!-- ngIf: ::( (skugroup.is_use_add_to_basket||sku.has_add_btn||abTests.addBtnBasket) && !sku.isOutOfStock() && !sku.noShipToCAorUS) -->
  <!-- ngIf: ::(sku.isOutOfStock() && !sku.noShipToCAorUS && skugroup.is_show_sign_up_for_email) -->
  <!-- ngIf: ::sku.noShipToCAorUS -->
</a>
'''

#productlist = soup.find('div',attrs={'class':"SkuGrid"})
#productlist = soup.find('a',attrs={'class':"u-size1of4.SkuItem.SkuItem--135"})
#productlist = soup.find('a',attrs={'class':"SkuItem--135"})
productlist = soup.find_all('div',attrs={'class':"SkuItem--135"})
#productlist = soup.find()
print len(productlist)
print productlist
#print productlist.findChildren()
#for child in children:
#    print child


# In[3]:

response.


# In[ ]:

def check_party_date(pdat,datecheck):
    #Extract the span that contains the date
    party_date = pdat.find('span',attrs={'class': 'views-field views-field-created'}).text.strip()
    return datetime.strptime(party_date,'%A, %B %d, %Y') < datecheck

def parse_product_lists(urlroot,pnum):
    productlinklist = [] 
    url = urlroot+'?currentPage='+str(pnum)
    print 'Parsing '+url
    #Grab the whole page
    #To handle the occasional 503 error, use a try statement and wait 5 seconds if HTTPError
    try:
        raw_page = urllib2.urlopen(url).read()
    except urllib2.HTTPError as e:
        print e.code
        time.sleep(5)
        raw_page = urllib2.urlopen(url).read()
    #Process the page w/ BeautifulSoup
    soup = BeautifulSoup(raw_page)
    partylist = soup.find('div',attrs={'class': 'view-content'})
    parties = partylist.find_all('div',attrs={'class': 'views-row'})
    for p in parties:
        # check the date to ensure it is before Dec 1, 2014
        if check_party_date(p,datetime(2014, 12, 1, 0,0)):
        # use the href link to get our link to the party
          party_link = urlroot+p.find('a').attrs['href']
        # skip the following odd link if it comes up
          if party_link != 'http://www.newyorksocialdiary.com/nysd/partypictures':
            # add to party link list
              partylinklist.append(party_link)
    return partylinklist

urlroot = 'http://www.sephora.com/search/search.jsp?keyword=hair&mode=all&node=1050092&sortBy=P_BEST_SELLING%3A1%3A%3AP_RATING%3A1%3A%3AP_PROD_NAME%3A0%3A%3AP_DEFAULT_SKU%3A1&pageSize=-1'
for page in np.arange(1,4):
    products = parse_product_lists(urlroot,page)
print parties[:15]


# In[4]:

raw_page = urllib2.urlopen(url).read()
print raw_page


# In[27]:

parties = partylist[0].find_all('a',attrs={'class': 'SkuItem--135'})
for p in parties:
    print p


# In[26]:

print len(partylist)


# In[49]:

print datetime.now().date()


# In[5]:

filelist=['files/sephora_hair_search_2017-01-18.xlsx',
'files/sephora_hair_search_2017-01-19.xlsx',
'files/sephora_hair_search_2017-01-23.xlsx',
'files/sephora_hair_search_2017-01-26.xlsx',
'files/sephora_hair_search_2017-01-28.xlsx',
'files/sephora_hair_search_2017-01-29.xlsx',
'files/sephora_hair_search_2017-02-01.xlsx',
'files/sephora_hair_search_2017-02-02.xlsx',
'files/sephora_hair_search_2017-02-05.xlsx',
'files/sephora_hair_search_2017-02-07.xlsx',
'files/sephora_hair_search_2017-02-09.xlsx']
all_df = pd.read_excel('files/sephora_hair_search_2017-01-14.xlsx')
for f in filelist:
    this_df=pd.read_excel(f)
    all_df=all_df.append(this_df,ignore_index=True)
print all_df.shape


# In[6]:

all_df.to_excel('files/sephora_hair_concat.xlsx',index=False)


# In[ ]:



