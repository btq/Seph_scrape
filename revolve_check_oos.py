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
    msg['Subject'] = 'REVOLVE OUT OF STOCK ALERT'
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


urlroot='http://www.revolve.com'
prod_urls=['/briogeo/br/2e2c0b/']
oos_flag=False
email_filename = 'oos_emails/revolve_oos_email_' + str(datetime.now().date()) + '.txt'

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
        prod_list=soup.find_all('li',attrs={'class':"js-plp-container"})
        
        for p in prod_list:
          link=p.find('a',attrs={'class':"js-plp-pdp-link"})
          hovr_btn=p.find('a',attrs={'class':"image-hover__btn image-hover__btn--focusable js-plp-quickview"})
          print link["href"], hovr_btn['aria-label']
          if hovr_btn.get_text(strip=True)=='PREORDER' or hovr_btn.get_text(strip=True)=='SOLD OUT':
            print ''
            oos_flag=True
            text_file.write("\nOOS: {0} {1}\n".format(urlroot+link["href"], hovr_btn['aria-label'].replace('PREORDER','').replace('SOLD OUT','')))


    text_file.close()                
    if oos_flag:
        #print 'email'
        email_nancy(email_filename)
    else:
        os.remove(email_filename)
        print email_filename, ' removed. No items OOS'

