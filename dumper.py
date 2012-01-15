#!/usr/bin/python
#coding=utf-8

# Joakim Axnér & Quentin Mazars-Simon


import json
import time
import os
import sys
from string import split
from time import sleep
from urllib2 import urlopen
from urllib2 import Request
from urllib2 import HTTPError


def fetch(username, category, fullname):
    limit = 100
    url = 'http://www.reddit.com/user/%s/%s/' % (username, category)
    url = '%s.json?limit=%s&after=%s' % (url, limit, fullname)
    req = Request(url)
    req.add_header('User-Agent', 'Reddit Post Recommender contact:qms@kth.se')
    
    return json.load(urlopen(url))
    
        
        
def fetch_all(username, category, most_recent_post):
    next_post = None
    filename = username + "-" + category + ".redditdata"
    output_directory = "output/" 
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    outputFile = open(output_directory + filename, 'w')
    is_first_time = True
    while True:
        page = fetch(username, category, next_post)
        start_time = time.time()
        #print(page)
        if('error' in page and page['error'] == 304):
            raise(Exception('Error304'))
        next_post = page['data']['after']
        #The JSON data is
        # converted to a native python "dictionary" by the json
        # module. It is similar to a nested array.
        # See http://docs.python.org/tutorial/datastructures.html#dictionaries
        for post in page['data']['children']:
            subreddit = post['data']['subreddit']
            post_id = post['data']['id']
            #If we already fetched this post, we should stop
            if(post_id == most_recent_post):
                # TODO: see how we should quit
                print('Already imported this!')
                next_post = None
                break
            #We store the most recent post (i.e. first link of the first json retrieved)
            if(is_first_time):
                most_recent_post = post_id
                is_first_time = False
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
            
            output_username_file = open('temp_userlist.txt', 'a')
            toWrite = username + ',' + category + ',' + str(most_recent_post) + '\r\n'
            output_username_file.write(toWrite)
            output_username_file.close()
            break
        
#Clean temp files that may be there from a previous run.
if os.path.exists("./temp_userlist.txt"):
    os.remove("./temp_userlist.txt")      
if(len(sys.argv) == 1 or (not sys.argv[1] == 'loop')):
    for line in open('userlist.txt'):
        # Unlike other programming languages, reading a line in python also
        # includes the newline character. So we need to remove it.
        
        username = line.rstrip('\r\n')
        most_recent_post = None
        try:
            fetch_all(username, 'liked', most_recent_post)
            fetch_all(username, 'disliked', most_recent_post)
            fetch_all(username, 'hidden', most_recent_post)
        except HTTPError as e:
            # TODO: Handle errors more intelligent
            # Currently skips username entirely if server returns error
            print('Server responded with %d. Skipping %s.' % (e.code, username))
            error_file = open('error_users.txt', 'a')
            error_file.write(username + '\n')
            error_file.close()
            continue
#        except:
#            print('Unexpected error: %s with %s' % (sys.exc_info()[0], username))
#            continue
        
else:  
    while True:
        for line in open('userlist2.txt'):
            # Unlike other programming languages, reading a line in python also
            # includes the newline character. So we need to remove it.
            
            line = line.rstrip('\r\n')
            splitted_line = split(line, ',')
            username = splitted_line[0]
            category = splitted_line[1]
            most_recent_post = splitted_line[2]
            
            try:
                fetch_all(username, category, most_recent_post)
                
            except HTTPError as e:
                # TODO: Handle errors more intelligently
                print('Server responded with %d. Skipping %s.' % (e.code, username))
                error_file = open('error_users.txt', 'a')
                error_file.write(username + '\n')
                error_file.close()
                continue
            except Exception as f:
                if (f.args[0] == "Error304"): #That is, not really an error, but we should try the user again later
                    print('Error 304: ' + username + " - " + category)
                    output_username_file = open('temp_userlist.txt', 'a')
                    toWrite = username + ',' + category + ',' + str(most_recent_post) + '\r\n'
                    output_username_file.write(toWrite)
                    output_username_file.close()
                    sleep(2)
                
                else:
                    print('Unexpected error: %s with %s' % (sys.exc_info()[0], username))
                    continue
        os.remove("./userlist2.txt")
        os.rename("./temp_userlist.txt", "./userlist2.txt")
        print('---')

