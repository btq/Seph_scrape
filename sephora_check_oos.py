import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

import smtplib
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
    #you = me
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
    fp = open('pass_file','rb')
    pswd = fp.read()
    fp.close()
    server.login("btquinn", pswd)

    server.sendmail(me, you, msg.as_string())
    server.quit()


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

if os.path.isfile(email_filename):
    print 'Already run and sent today'
else:
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
    else:
        os.remove(email_filename)
        print email_filename, ' removed. No items OOS'

