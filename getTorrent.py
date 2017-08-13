
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


def searchTorrent():

	#Testing server availability
	host=cfg['server']['website']
	r= requests.get(host)
	if(r.status_code != requests.codes.ok):
        	print("cannot connect to "+host)
       		sys.exit(2)


	#Define the string to search
	search=input(' What do you want to search ?\n')

	print("you're search is "+search)
	URL=host+"/search/"+search+"/0/99/0"

	r= requests.get(URL)
	if(r.status_code == requests.codes.ok):
        	 text='OK'
#       	 print(r.status_code)
	else:
        	print("cannot query this URL "+URL)
        	sys.exit(2)

	soup = BeautifulSoup(r.text,"html5lib")
	torrents= soup.find_all('a',href=re.compile('torrent'))

	stat=soup.find_all('td',align="right")
	magnetInfo=soup.find_all('a',href=re.compile("magnet"))
	sizeInfo=soup.find_all('font',class_='detDesc')
	#sizeInfo=soup.find_all('font',class="detDesc")

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
#               	print("Magnet : "+magnetInfo[i]['href'])
                	table.add_row([str(j+1),name,se,le,size])
                	j=j+1

        	i=i+1
	print(table)
	choice=input("Select your torrent ( 1 to "+str(j)+")\n")
	while(int(choice) < 0 or int(choice) > j):

        	choice=input("Select your torrent ( 1 to "+str(j)+")\n")

	magnet=magnetInfo[int(choice)-1]['href']
	tc=transmissionrpc.Client('localhost',port=9091)
	tc.add_torrent(magnet)


def listTorrents():

	tc=transmissionrpc.Client('localhost',port=9091)
	torrents=tc.get_torrents()
	print("test "+str(torrents))
	tableTorrent=PrettyTable(['No','Name','Status','Size','Speed','Estimated end'])
	i=1
	for t in torrents:
		if(t.status=='Downloading'):
			tableTorrent.add_row([str(i),str(t.name),str(t.status),str(t.totalSize),str(t.rateDownload),str(t.eta)])
		
		else:
	
			tableTorrent.add_row([str(i),str(t.name),str(t.status),str(t.totalSize),str(t.rateDownload),str("N/A")])
		i=i+1
	return tableTorrent

def removeTorrent():
	table=listTorrents()
	tc=transmissionrpc.Client('localhost',port=9091)
	torrents=tc.get_torrents()
	print(table)
	action=input("Which torrent needs to be deleted ? (0 = quit)")
	while(int(action)<0 or int(action)>len(action)):
		action=input("Which torrent needs to be deleted ? (0 = quit)")
	torrent=torrents[int(action)-1]
	tc.stop_torrent(torrent.hashString)

######MAIN##########
print("test")
table=PrettyTable(['No','Action'])
table.add_row(['1','Search torrent'])
table.add_row(['2','List torrent'])
table.add_row(['3','Remove active torrent'])
print(table)


action=input("Which action ? (0 = quit)\n")
while(int(action)<0 or int(action)>3):
	action=input("Which action ? (0 = quit)")

print(action)	
if(action=='0'):
	sys.exit(2)
if(action=='1'):
	print("Searching torrent")
	searchTorrent()
	print(result)
if(action=='2'):
	print("Listing torrent")
	result=listTorrents()
	print(result)
	#tc.remove_torrent(hashTorrent)
if(action=='3'):
	print("Remove Torrent")
	removeTorrent()	
sys.exit(2)



