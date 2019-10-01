#!/bin/sh
PATH=/Users/bquinn206/anaconda/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin
cd /Users/bquinn206/GitHub/Seph_scrape
python sephora_check_oos.py
python sephora_check_oos_can.py
python revolve_check_oos.py
