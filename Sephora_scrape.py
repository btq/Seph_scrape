
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


# In[2]:

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


# In[2]:

import json
import requests
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from bs4 import BeautifulSoup

urlroot = 'http://www.sephora.com/search/search.jsp?keyword=hair&mode=all&node=1050092&sortBy=P_BEST_SELLING%3A1%3A%3AP_RATING%3A1%3A%3AP_PROD_NAME%3A0%3A%3AP_DEFAULT_SKU%3A1&pageSize=-1'
page=1
url=urlroot
print 'Parsing' + url
response = requests.get(url)
soup = BeautifulSoup(response.content,"lxml")
data = soup.find('script',attrs={'id':"searchResult"}).get_text()
jsondata = json.loads(data)
    


# In[14]:

with open('jsondata.txt', 'w') as outfile:
    json.dump(data, outfile)


# In[7]:

print jsondata.keys()


# In[6]:

print jsondata['products'].keys()


# In[8]:

print jsondata['meta'].keys()


# In[ ]:


df=pd.DataFrame(jsondata['products']['products'])
df['date_scraped']=datetime.now()
return df

urlroot = 'http://www.sephora.com/search/search.jsp?keyword=hair&mode=all&node=1050092&sortBy=P_BEST_SELLING%3A1%3A%3AP_RATING%3A1%3A%3AP_PROD_NAME%3A0%3A%3AP_DEFAULT_SKU%3A1&pageSize=-1'
page=1
url=urlroot
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


# In[2]:

urlroot = 'http://www.sephora.com'
page1='/rosarco-oil-P388629'
page2='/blossom-bloom-ginseng-biotin-volumizing-shampoo-P402071'
url = urlroot + str(page1)
print 'Parsing' + url
response = requests.get(url)
soup = BeautifulSoup(response.content,"lxml")


# In[4]:

print soup.find('b',attrs={'class','u-textWarning'})


# In[9]:

print soup.find('script')


# In[10]:

soup.find_all('script')


# In[5]:

urlroot = 'http://www.sephora.com'
page1='/rosarco-oil-P388629'
page2='/blossom-bloom-ginseng-biotin-volumizing-shampoo-P402071'
url2 = urlroot + str(page2)
print 'Parsing ' + url2
response2 = requests.get(url2)
soup2 = BeautifulSoup(response.content,"lxml")


# In[6]:

print soup.find('b',attrs={'class','u-textWarning'})


# In[ ]:

data = soup.find('script',attrs={'id':"searchResult"}).get_text()
jsondata = json.loads(data)
df=pd.DataFrame(jsondata['products']['products'])


# In[3]:

oos_item='https://www.sephora.com/product/dont-despair-repair-deep-conditioning-mask-P388628?skuId=1784636'
is_item='https://www.sephora.com/product/dont-despair-repair-deep-conditioning-mask-P388628?skuId=1823418'
resp_oos=requests.get(oos_item)
resp_is=requests.get(is_item)


# In[13]:

import re
print re.search('Stock',resp_oos.content)
print re.search('Stock',resp_is.content)


# In[15]:

with open("oos.txt", "w") as text_file:
    text_file.write("{}".format(resp_oos.content))
    
with open("is.txt", "w") as text_file:
    text_file.write("{}".format(resp_is.content))


# In[16]:

soup = BeautifulSoup(resp_oos.content,"lxml")
data = soup.find_all('button')
    


# In[17]:

print soup.find('script',attrs={'id':"searchResult"}).get_text()


# In[34]:

for link in soup.find_all('script'):
    if "Sephora.Util.InflatorComps.queue('RegularProductTop'," in link.get_text():
        #print link.get_text()[55:-16]
        json_string=link.get_text()[55:-16].replace('\\"','"').replace("\\'","'").replace('\\"','"')
        print json_string
        jsondata = json.loads(json_string)
        #print jsondata
        #df=pd.DataFrame(jsondata['products']['products'])


# In[33]:

print json_string[15690:15700]


# In[48]:

print jsondata.keys()


# In[38]:

print len(jsondata['currentProduct'])
print jsondata['currentProduct'].keys()


# In[49]:

print jsondata['currentProduct']['imageAltText']


# In[42]:

print len(jsondata['currentProduct']['regularChildSkus'])


# In[46]:

print jsondata['currentProduct']['regularChildSkus'][0]


# In[45]:

print jsondata['currentProduct']['regularChildSkus'][0]['isOutOfStock']


# In[47]:

for sku in jsondata['currentProduct']['regularChildSkus']:
    print sku['targetUrl'], sku['skuName'], sku['isOutOfStock']
    if sku['isOutOfStock']:
        with open("oos_alert_email.txt", "w") as text_file:
            text_file.write("{0}".format())


# In[80]:

urlroot='http://sephora.com'
prod_urls=['/product/dont-despair-repair-deep-conditioning-mask-P388628',
'/product/scalp-revival-charcoal-coconut-oil-micro-exfoliating-shampoo-P418507',
'/product/rosarco-milk-reparative-leave-in-conditioning-spray-P396733',
'/product/scalp-revival-charcoal-tea-tree-scalp-treatment-P418506',
'/product/rosarco-blow-dry-perfection-heat-protectant-creme-P411359',
'/product/blossom-bloom-ginseng-biotin-volumizing-conditioner-P388625',
'/product/blossom-bloom-ginseng-biotin-volumizing-shampoo-P402071',
'/product/scalp-revival-charcoal-biotin-dry-shampoo-P418505',
'/product/be-gentle-be-kind-avocado-quinoa-co-wash-P388623',
'/product/curl-charisma-rice-amino-avocado-leave-in-defining-creme-P388626',
'/product/rosarco-repair-conditioner-P402073',
'/product/be-gentle-be-kind-green-tea-clarifying-shampoo-P388624',
'/product/curl-charisma-definition-on-the-go-travel-kit-P422368',
'/product/rosarco-repair-shampoo-P402072',
'/product/rosarco-repair-on-the-go-travel-kit-P422369',
'/product/curl-charisma-rice-amino-quinoa-frizz-control-gel-P408411',
'/product/curl-charisma-rice-amino-shampoo-P402074',
'/product/curl-charisma-rice-amino-shea-curl-defining-conditioner-P388627',
'/product/blossom-bloom-volumizing-on-the-go-travel-kit-P422370',
'/product/rosarco-oil-P388629',
'/product/don-t-despair-repair-gel-to-oil-overnight-repair-treatment-P408248',
'/product/blossom-bloom-ginseng-biotin-volumizing-spray-P396734',
'/product/ultimate-hair-goals-best-briogeo-kit-P425022',
'/product/rosarco-repair-winter-hair-renewal-P425021']
oos_flag=False
email_filename = 'oos_email_' + str(datetime.now().date()) + '.txt'
import os.path

if ~os.path.isfile(email_filename):

    text_file = open(email_filename, "w")

    for p in prod_urls:
        print p
        resp=requests.get(urlroot+p)
        soup = BeautifulSoup(resp.content,"lxml")
        for link in soup.find_all('script'):
            if "Sephora.Util.InflatorComps.queue('RegularProductTop'," in link.get_text():
                #print link.get_text()[55:-16]
                json_string=link.get_text()[55:-16].replace('\\"','"').replace("\\'","'").replace('\\"','"')
                #print json_string
                jsondata = json.loads(json_string)
                if 'regularChildSkus' in jsondata['currentProduct'].keys():
                    field='regularChildSkus'
                    for sku in jsondata['currentProduct'][field]:
                        print sku['targetUrl'], sku['skuName'], sku['isOutOfStock']
                        if sku['isOutOfStock']:
                            oos_flag=True
                            text_file.write("\nOOS: {0} {1} {2}\n".format(urlroot+sku['targetUrl'], sku['skuName'], sku['isOutOfStock']))
                else:
                    field='currentSku'
                    sku=jsondata['currentProduct'][field]
                    print sku['targetUrl'], sku['isOutOfStock']
                    if sku['isOutOfStock']:
                        oos_flag=True
                        text_file.write("\nOOS: {0} {1}\n".format(urlroot+sku['targetUrl'], sku['isOutOfStock']))


    text_file.close()                
    if oos_flag:
        email_nancy(email_filename)


# In[78]:

#print jsondata['currentProduct'][field]
#print jsondata['currentProduct'].keys()
#print jsondata['currentProduct']['currentSku']
with open("curltravel.txt", "w") as text_file:
    text_file.write("{}".format(resp.content))


# In[58]:

print "OOS: {0} {1} {2}".format(urlroot+sku['targetUrl'], sku['skuName'], sku['isOutOfStock'])
text_file = open(email_filename, "w")
text_file.write("\nOOS: {0} {1} {2}\n".format(urlroot+sku['targetUrl'], sku['skuName'], sku['isOutOfStock']))
text_file.close()


# In[90]:

import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def email_nancy(text_file):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    fp = open(text_file, 'rb')
    # Create a text/plain message
    msg = MIMEText(fp.read())
    fp.close()

    me = 'btquinn@gmail.com'
    you ='orders@briogeohair.com'
    msg['Subject'] = 'SEPHORA OUT OF STOCK ALERT'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    #Next, log in to the server
    server.login("btquinn", "ilC.20090521")

    server.sendmail(me, you, msg.as_string())
    server.quit()


# In[91]:

email_nancy(email_filename)


# In[82]:

import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)

#Next, log in to the server
server.login("btquinn", "ilC.20090521")

#Send the mail
msg = '''
Hello!''' # The /n separates the message from the headers
server.sendmail("btquinn@gmail.com", "nancy@briogeohair.com", msg)


# In[83]:

server.ehlo()
server.starttls()
server.ehlo()


# In[85]:

server.login("btquinn", "ilC.20090521")


# In[86]:

msg = '''
Hello!''' # The /n separates the message from the headers
server.sendmail("btquinn@gmail.com", "nancy@briogeohair.com", msg)


# In[99]:

import os
if not os.path.isfile(email_filename):
    print 'no file'


# In[ ]:



