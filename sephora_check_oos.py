import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

import urllib3
urllib3.disable_warnings()

def email_nancy(text_file):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    fp = open(text_file, 'rb')
    # Create a text/plain message
    msg = MIMEText(fp.read())
    fp.close()

    me = 'btquinn@gmail.com'
    you ='orders@briogeohair.com'
    #you = me
    msg['Subject'] = 'SEPHORA USA OUT OF STOCK ALERT'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    #Next, log in to the server
    fp = open('pass_file','rb')
    pswd = fp.read()
    fp.close()
    server.login("btquinn", pswd)

    server.sendmail(me, you, msg.as_string())
    server.quit()


urlroot='https://sephora.com'
prod_urls=['/product/dont-despair-repair-deep-conditioning-mask-P388628',
'/product/scalp-revival-charcoal-coconut-oil-micro-exfoliating-shampoo-P418507',
'/product/hair-o-scopes-brightest-stars-bestsellers-P435405',
'/product/superfoods-shampoo-conditioner-hair-pack-P431542',
'/product/rosarco-milk-reparative-leave-in-conditioning-spray-P396733',
'/product/blossom-bloom-ginseng-biotin-volumizing-shampoo-P402071',
'/product/scalp-revival-charcoal-tea-tree-scalp-treatment-P418506',
'/product/don-t-despair-repair-super-moisture-shampoo-P427718',
'/product/rosarco-blow-dry-perfection-heat-protectant-creme-P411359',
'/product/scalp-revival-charcoal-peppermint-oil-cooling-jelly-conditioner-P429961',
'/product/blossom-bloom-ginseng-biotin-volumizing-conditioner-P388625',
'/product/don-t-despair-repair-strength-moisture-leave-in-mask-P427526',
'/product/rosarco-repair-conditioner-P402073',
'/product/be-gentle-be-kind-kale-apple-replenishing-superfood-conditioner-P431544',
'/product/scalp-revival-charcoal-biotin-dry-shampoo-P418505',
'/product/be-gentle-be-kind-avocado-quinoa-co-wash-P388623',
'/product/be-gentle-be-kind-matcha-apple-replenishing-superfood-shampoo-P431543',
'/product/scalp-revival-charcoal-coconut-oil-micro-exfoliating-shampoo-mini-P427715',
'/product/curl-charisma-rice-amino-shampoo-P402074',
'/product/curl-charisma-rice-amino-shea-curl-defining-conditioner-P388627',
'/product/dont-despair-repair-deep-conditioning-hair-cap-system-P425409',
'/product/blossom-bloom-ginseng-biotin-volumizing-spray-P396734',
'/product/rosarco-milk-tm-reparative-leave-in-conditioning-spray-mini-P426205',
'/product/rosarco-repair-shampoo-P402072',
'/product/curl-charisma-rice-amino-avocado-leave-in-defining-creme-P388626',
'/product/rosarco-oil-P388629',
'/product/curl-charisma-rice-amino-quinoa-frizz-control-gel-P408411',
'/product/don-t-despair-repair-gel-to-oil-overnight-repair-treatment-P408248',
'/product/curl-charisma-chia-flax-seed-coil-custard-P435402',
'/product/rose-quartz-crystal-energy-comb-P433174',
'/product/scalp-revival-scalp-massager-P429962',
'/product/don-rsquo-t-despair-repair-tm-deep-conditioning-mask-mini-P426204']
oos_flag=False
email_filename = 'oos_emails/sephora_usa_oos_email_' + str(datetime.now().date()) + '.txt'

if os.path.isfile(email_filename):
    print 'Already run and sent today'
else:
    text_file = open(email_filename, "w")

    for p in prod_urls:
        print p
        try:
            resp=requests.get(urlroot+p,verify=False)
        except (requests.HTTPError, requests.ConnectionError), error:
            os.remove(email_filename)
            raise
            exit()
        soup = BeautifulSoup(resp.content,"lxml")
        data = soup.find('script',attrs={'id':"linkJSON"}).get_text()
        output = json.loads(data)

        for d in output:
            if d['path']=='RegularProductTop':
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
    if oos_flag:
        #print 'email'
        email_nancy(email_filename)
    else:
        os.remove(email_filename)
        print email_filename, ' removed. No items OOS'

