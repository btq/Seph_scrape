'''
every module in the system must use the following import:

from utils import log

'''
import os
import sys
import re
import logging
from subprocess import Popen, PIPE
from configparser import ConfigParser

#log_format = '%(asctime)s %(levelname)-8s [%(filename)s,%(lineno)d] %(message)s'
#logging.basicConfig(level=logging.DEBUG, format=log_format)
log = logging.getLogger('scraper')


CSS = '''

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

'''

def error(msg):
    log.error(msg + '. Exiting ...')
    sys.exit(1)


''' 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
'''

