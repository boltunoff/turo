# turo

Turo Data Scrapping

The project is for personal use. It's purpose is to collect price data from turo.com web page. All the scripts comply with Turo policy and abide robots.txt
Currently, it is used to collect daily prices for minivans listed on Turo, and write it to a CSV file.


Steps to set up the environment and execute the script on Linux EC2 machine:
1. Git clone the repo

2. Extract Linux version of phantomjs by running (included in git repo):
    tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2

3. Copy executable phantomjs
    from /home/ec2-user/turo/phantomjs-2.1.1-linux-x86_64/bin/phantomjs
    to /usr/local/bin
    run:
    cp /home/ec2-user/turo/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin

4. Create(a) and activate(b) python virtual environment. Install Python libraries(c) by running:
    a) cd /home/ec2-user/turo
       virtualenv myenv
    b) source myenv/bin/activate
    c) pip install -r requirements.txt

5. Execute python script:
   python genr_turo_parse.py

6. Find your log file and output file in:
   /home/ec2-user/turo/
   turotask_minivans.log
   turo_minivans_data.csv


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