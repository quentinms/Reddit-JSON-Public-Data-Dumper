#! /bin/bash

#Quentin Mazars-Simon

# Column number - Info we have - Description
# 1 - username - Username of the user (Thanks captain Obvious!)
# 2 - vote - What the user has voted: up (1), down (-1) or hidden (0)
# 3 - post_id - The unique id of the post
# 4 - subreddit - Subreddit of the post
# 5 - url - The link to the post (to the original content, not to reddit)
# 6 - author - Person who created the post
# 7 - date - Unix timestamp of when the post was created
# 8 - title - The title of the post
# 9 - thumbnail - The url to the thumbnail of the post (if not, it is equal to 'None')

for item in ./output/*.redditdata
do 
# Create file to be imported in the "correspondance table" (see in URD)
# We need username, post_id, vote 
cut -f 1,3,2 "$item" >> correspondance_table.csv

# Create file to be imported in the "post table" (see in URD)
# We need post_id, subreddit, url, author, date, title, thumbnail
cut -f 3,4,5,6,7,8,9 $item >> posts_table.csv
done

# TODO: Import into postgreSQL database. (see COPY: http://wiki.postgresql.org/wiki/COPY)

#rm posts_table.csv
#rm correspondance_table.csv
