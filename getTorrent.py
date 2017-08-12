import requests
import yaml

#Importing configuration file
with open("configurationFile.yaml","r") as ymlfile:
	cfg=yaml.load(ymlfile)


#Testing server availability
r= requests.get(cfg['server']['website'])
if(r.status_code == requests.codes.ok):
	print(r.status_code)
else:
	print("cannot connect to "+cfg['server']['website'])
	sys.exit(2)

#Define the string to search
search=input(' What do you want to search ?\n')

print("you're search is "+search)

print("hello world")
