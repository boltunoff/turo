# turo

Turo Google Calendar ... description following... 



Steps to set up the environment and execute the script on Linux EC2 machine:
1. Git clone the repo

2. 

3. 
4. Create(a) and activate(b) python virtual environment. .....

Cron schedule:

SHELL=/bin/bash
MAILTO=boltunoff@yahoo.com
### adding path for phantomjs to be found by cron
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# cron is running at -6 hours
21 14 * * * source ~/myenv/bin/activate; cd turo; python genr_turo_parse.py

# * * * * * Command to be executed
# - - - - -
# | | | | |
# | | | | +----- Day of week (0-7)
# | | | +------- Month (1 - 12)
# | | +--------- Day of month (1 - 31)
# | +----------- Hour (0 - 23)
#  +------------- Min (0 - 59)
