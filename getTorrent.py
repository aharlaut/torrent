import requests
import yaml
import xmltodict
import re
import texttable
import itertools
import sys

from bs4 import BeautifulSoup
#Importing configuration file
with open("configurationFile.yaml","r") as ymlfile:
	cfg=yaml.load(ymlfile)


#Testing server availability
host=cfg['server']['website']
r= requests.get(host)
if(r.status_code == requests.codes.ok):
	test='OK'
#	print(r.status_code)
else:
	print("cannot connect to "+host)
	sys.exit(2)


#Define the string to search
search=input(' What do you want to search ?\n')

print("you're search is "+search)
URL=host+"/search/"+search+"/0/99/0"

r= requests.get(URL)
if(r.status_code == requests.codes.ok):
	 text='OK'
#        print(r.status_code)
else:
        print("cannot query this URL "+URL)
        sys.exit(2)

soup = BeautifulSoup(r.text,"html5lib")
torrent= soup.find_all('a',href=re.compile('torrent'))

stat=soup.find_all('td',align="right")
i=0
for t in torrent:
	print(t.getText())
	print("Seeder : "+stat[i].getText())
	print("Leeacher : "+stat[i+1].getText())
	i=i+1
	
sys.exit(2)



