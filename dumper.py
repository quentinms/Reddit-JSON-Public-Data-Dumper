# Joakim Axner & Quentin Mazars-Simon
# TODO: Add acute e to Joakim's name.
#!/usr/bin/python

import json
import time
import os
from time import sleep
from urllib2 import urlopen
from urllib2 import HTTPError


def fetch(username, category, fullname):
    limit = 100
    url = 'http://www.reddit.com/user/%s/%s/' % (username, category)
    url = '%s.json?limit=%s&after=%s' % (url, limit, fullname)
    return json.load(urlopen(url))

def fetch_all(username, category):
    next = None
    filename = username+"-"+category+".redditdata"
    output_directory="output/" 
    if not os.path.exists(output_directory):
	os.makedirs(output_directory)
    outputFile = open(output_directory+filename,'w')

    while True:
        page = fetch(username, category, next)
        start_time = time.time()
        next = page['data']['after']
        #The JSON data is
        # converted to a native python "dictionary" by the json
        # module. It is similar to a nested array.
        # See http://docs.python.org/tutorial/datastructures.html#dictionaries
	for post in page['data']['children']:
            	subreddit = post['data']['subreddit']
            	id = post['data']['id']
            	title = post['data']['title']
            	thumbnail = post['data']['thumbnail']
            	url = post['data']['url']
		author = post['data']['author']
		date = post['data']['created_utc']
            	# We have to make sure the thumbnail_url field exists.
		if(thumbnail == "" and post['data']['media'] != None and 'oembed' in post['data']['media'] and 'thumbnail_url' in post['data']['media']['oembed']):
			thumbnail = post['data']['media']['oembed']['thumbnail_url']
       	    	if(not thumbnail.startswith("http")): thumbnail = "None"
	    	# TODO: Handle ", ', e acute, e grave, etc. in titles (and other fields?).
		toWrite = str(id)+"\t"+subreddit+"\t"+url+"\t"+author+"\t"+str(date)+"\t"+title+"\t"+thumbnail+"\n"
		try:
			outputFile.write(toWrite)
		except:
			print("Error with:"+toWrite)
	
        if (next == None):
		outputFile.close()
		break
 	# reddit API rules demands this
        sleep((2000-(time.time()-start_time))/1000)

for line in open('userlist.txt'):
    # Unlike other programming languages, reading a line in python also
    # includes the newline character. So we need to remove it.
	username = line.rstrip('\r\n')
   	try:
        	fetch_all(username, 'liked')
        	fetch_all(username, 'disliked')
        	fetch_all(username, 'hidden')
    	except HTTPError as e:
        	# TODO: Handle errors more intelligent
        	# Currently skips username entirely if server returns error
        	print('Server responded with %d. Skipping %s.' % (e.code, username))
        	continue

