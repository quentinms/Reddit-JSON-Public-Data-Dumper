#!/usr/bin/python
#coding=utf-8

# Joakim Axnér & Quentin Mazars-Simon


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
    next_post = None
    filename = username + "-" + category + ".redditdata"
    output_directory = "output/" 
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    outputFile = open(output_directory + filename, 'w')

    while True:
        page = fetch(username, category, next_post)
        start_time = time.time()
        next_post = page['data']['after']
        #The JSON data is
        # converted to a native python "dictionary" by the json
        # module. It is similar to a nested array.
        # See http://docs.python.org/tutorial/datastructures.html#dictionaries
        for post in page['data']['children']:
            subreddit = post['data']['subreddit']
            post_id = post['data']['id']
            title = post['data']['title']
            thumbnail = post['data']['thumbnail']
            url = post['data']['url']
            author = post['data']['author']
            date = post['data']['created_utc']
            # We have to make sure the thumbnail_url field exists.
            if(thumbnail == "" and post['data']['media'] != None and 'oembed' in post['data']['media'] and 'thumbnail_url' in post['data']['media']['oembed']):
                thumbnail = post['data']['media']['oembed']['thumbnail_url']
            if(not thumbnail.startswith("http")): thumbnail = "None"
       
            toWrite = str(post_id) + "\t" + subreddit + "\t" + url + "\t" + author + "\t" + str(date) + "\t" + title + "\t" + thumbnail + "\n"
            try:
                outputFile.write(toWrite)
            except:
                print("Error with:" + toWrite)

        # reddit API rules demands 2 sec wait between each request.
        sleep((2000 - (time.time() - start_time)) / 1000)

        if (next_post == None):
            print("Done with: " + username + " " + category)
            outputFile.close()
            break
 
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

