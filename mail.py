from utils import log
from os.path import basename, isfile
import re
from datetime import datetime
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

def send_email(sender, subject, message, to='', cc='', bcc='', files=None, high_importance=False,  server='localhost', verbose=True):
    
    message_type = 'html' if '<html>' in message.lower() else 'plain'
    
    msg = MIMEMultipart()
        
    msg['From'] = sender
    msg['Subject'] = subject
    msg['To'] = to
    msg['CC'] = cc
    msg['BCC'] = bcc

    msg.attach(MIMEText(message, message_type))

    for f in files or []:
        if '|' in f:
            file_name, attachement_name = f.split('|')[:2]
        else:
            file_name = attachement_name = f
        if not isfile(file_name):
            #print('attachment not found: %s', file_name)
            log.warning('attachment not found: %s', file_name)
            continue
        
        with open(file_name, "rb") as fh:
            #part = MIMEApplication(fh.read(),Name=basename(f))
            part = MIMEApplication(fh.read(),Name=basename(file_name))
            #part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            part['Content-Disposition'] = 'attachment; filename="%s"' % attachement_name
            msg.attach(part)

    if high_importance:
        msg['Importance'] = 'High'

    receivers = re.split('\s*,\s*', to) + re.split('\s*,\s*', cc) + re.split('\s*,\s*', bcc)
    if verbose:
        #print('sending an email from %s to %s with subject "%s" message:\n%s', sender, receivers, subject, message)
        log.info('sending an email from %s to %s with subject "%s" message:\n%s', sender, receivers, subject, message)

    if not receivers:
        raise AttributeError('no senders given ; failed to send an email')
        
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()

if __name__ == '__main__':
    response1 = send_email('briogeods@gmail.com', '[test] my subject %s' % datetime.now(), 'line1\nline2',
        to='btquinn@gmail.com', bcc='' )
    print(response1)
    response2 = send_email('briogeods@gmail.com', '[test html] my subject %s' % datetime.now(), '''
<html><head><style>

table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}

th, td {
    padding: 3px 20px;
}

.bold {
    font-weight: bold;
}

.red {
    color: red;
}

.fail {
    font-style: italic;
    font-weight: bold;
    color: red;
}

</style></head><body>
<table>
<tr><th>Retailer</th><th>Product</th><th>Size</th><th>Link</th></tr>
<tr><th>Sephora.com</th><th>Shampoo</th><th>8 oz.</th><th>http://sephora.com</th></tr>
</table>
</body>
<html>

'''
        ,to='btquinn@gmail.com', bcc='' )
    print(response2)



