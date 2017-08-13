import requests
import yaml
import xmltodict
import re
import texttable
import itertools
import sys
from prettytable import PrettyTable
from bs4 import BeautifulSoup
import transmissionrpc

class OutColors:
    DEFAULT = '\033[0m'
    BW = '\033[1m'
    LG = '\033[0m\033[32m'
    LR = '\033[0m\033[31m'
    SEEDER = '\033[1m\033[32m'
    LEECHER = '\033[1m\033[31m'


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
torrents= soup.find_all('a',href=re.compile('torrent'))

stat=soup.find_all('td',align="right")
magnetInfo=soup.find_all('a',href=re.compile("magnet"))
sizeInfo=soup.find_all('font',class_='detDesc')
#sizeInfo=soup.find_all('font',class="detDesc")

print(sizeInfo)

i=0
j=0
numResult=len(torrents)
table=PrettyTable(['No','Name','Seeders','Leechers','Size'])
for t in torrents:
	
	name=t.getText()
	if(name):
		se=stat[i].getText()
		le=stat[i+1].getText()
		size=sizeInfo[j].getText().split(',')[1].split("Size")[1]
		#print(str(i)+" : "+str(name)+" Seeders : "+str(se)+" Leechers : "+str(le)+" "+str(size))
#		print("Magnet : "+magnetInfo[i]['href'])
		table.add_row([str(j+1),name,se,le,size])
		j=j+1

	i=i+1
print(table)
choice=input("Select your torrent ( 1 to "+str(j)+")\n")
while(int(choice) < 0 or int(choice) > j):
	
	choice=input("Select your torrent ( 1 to "+str(j)+")\n")

magnet=magnetInfo[int(choice)-1]['href']
tc=transmissionrpc.Client('localhost',port=9091)
#tc.add_torrent(magnet)

torrents=tc.get_torrents()
for t in torrents:
	print(t.name)
	print(t.status)
	print(t.eta)
	print(t.rateDownload)
	hashTorrent=t.hashString
	tc.remove_torrent(hashTorrent)
	
sys.exit(2)



