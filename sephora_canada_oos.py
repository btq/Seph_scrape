
# coding: utf-8

# In[1]:

import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText



# In[2]:

urlroot='https://sephora.ca'
prod_urls=['/product/scalp-revival-charcoal-coconut-oil-micro-exfoliating-shampoo-P418507',
'/product/dont-despair-repair-deep-conditioning-mask-P388628',
'/product/dont-despair-repair-deep-conditioning-hair-cap-system-P425409',
'/product/don-t-despair-repair-super-moisture-shampoo-P427718',
'/product/scalp-revival-charcoal-tea-tree-scalp-treatment-P418506',
'/product/don-t-despair-repair-strength-moisture-leave-in-mask-P427526',
'/product/rosarco-milk-reparative-leave-in-conditioning-spray-P396733',
'/product/rosarco-blow-dry-perfection-heat-protectant-creme-P411359',
'/product/blossom-bloom-ginseng-biotin-volumizing-shampoo-P402071',
'/product/scalp-revival-charcoal-biotin-dry-shampoo-P418505',
'/product/rosarco-repair-conditioner-P402073',
'/product/blossom-bloom-ginseng-biotin-volumizing-conditioner-P388625',
'/product/rosarco-milk-tm-reparative-leave-in-conditioning-spray-mini-P426205',
'/product/curl-charisma-rice-amino-avocado-leave-in-defining-creme-P388626',
'/product/blossom-bloom-ginseng-biotin-volumizing-spray-P396734',
'/product/rosarco-repair-shampoo-P402072',
'/product/be-gentle-be-kind-avocado-quinoa-co-wash-P388623',
'/product/revive-repair-scalp-hair-power-duo-P427719',
'/product/rosarco-oil-P388629',
'/product/don-t-despair-repair-gel-to-oil-overnight-repair-treatment-P408248',
'/product/curl-charisma-rice-amino-quinoa-frizz-control-gel-P408411',
'/product/be-gentle-be-kind-green-tea-clarifying-shampoo-P388624',
'/product/curl-charisma-definition-on-the-go-travel-kit-P422368',
'/product/curl-charisma-rice-amino-shampoo-P402074',
'/product/rosarco-repair-on-the-go-travel-kit-P422369',
'/product/curl-charisma-rice-amino-shea-curl-defining-conditioner-P388627',
'/product/blossom-bloom-volumizing-on-the-go-travel-kit-P422370',
'/product/scalp-revival-charcoal-coconut-oil-micro-exfoliating-shampoo-mini-P427715',
'/product/don-rsquo-t-despair-repair-tm-deep-conditioning-mask-mini-P426204']
oos_flag=False


# In[5]:

email_filename = 'oos_email_can' + str(datetime.now().date()) + '.txt'

if os.path.isfile(email_filename):
    print('Already run and sent today')
else:
    text_file = open(email_filename, "w")
    for p in prod_urls:
        print(p)
        try:
            resp=requests.get(urlroot+p+'?country_switch=ca&lang=en')
        except(requests.HTTPError, requests.ConnectionError), error:
            os.remove(email_filename)
            raise
            exit()
        soup = BeautifulSoup(resp.content,"lxml")
        data = soup.find('script',attrs={'id':"linkJSON"}).get_text()
        output = json.loads(data)
        for d in output:
            if d['path']=='ProductPage/Type/RegularProduct/RegularProductTop':
                prod=d['props']['currentProduct']
                if 'regularChildSkus' in prod.keys():
                    field='regularChildSkus'
                    for sku in prod[field]:
                        print sku['targetUrl'], sku['skuName'], ' OOS:', sku['isOutOfStock'], ' FewLeft:', sku['isOnlyFewLeft']
                        if sku['isOutOfStock']:
                            oos_flag=True
                            text_file.write("\nOOS: {0} {1}\n".format(urlroot+sku['targetUrl'], sku['skuName']))
                        if sku['isOnlyFewLeft']:
                            oos_flag=True
                            text_file.write("\mFEW_LEFT: {0} {1}\n".format(urlroot+sku['targetUrl'], sku['skuName']))
                else:
                    field='currentSku'
                    sku=prod[field]
                    print sku['targetUrl'], ' OOS:', sku['isOutOfStock'], ' FewLeft:', sku['isOnlyFewLeft']
                    if sku['isOutOfStock']:
                        oos_flag=True
                        text_file.write("\nOOS: {0}\n".format(urlroot+sku['targetUrl']))
                    if sku['isOnlyFewLeft']:
                        oos_flag=True
                        text_file.write("\nFEW_LEFT: {0}\n".format(urlroot+sku['targetUrl']))
    text_file.close()                
    #if oos_flag:
        #print 'email'
    #    email_nancy(email_filename)
    #else:
    #    os.remove(email_filename)
    #    print email_filename, ' removed. No items OOS'



# In[ ]:



