#!/bin/bash

#get the .json of the user
getJSON()
{
	
	if [ ${from_number} -gt 0 ]; then
	data=`curl -s "http://www.reddit.com/user/${LINE}/liked/.json?limit=${NB_POSTS}&after=${from_postID}&count=${from_number}"`
	echo ${data} > "$PWD/json/TEST-${LINE}-${from_number}.json";
	else
	data=`curl -s "http://www.reddit.com/user/${LINE}/liked/.json?limit=${NB_POSTS}"`
	echo ${data} > "$PWD/json/TEST-${LINE}.json";
	fi
	
	let from_number+=${NB_POSTS}
	
	#get the id of the next post.
	from_postID=`echo ${data} | sed -E 's/.*\"after\":.\"?([^\".]*)\"?,.*/\1/'`
	
	#In case of 404...
	if [ "${from_postID}" = "{error: 404}" ]; then
	out_of_date_users=${out_of_date_users}"\n"${username}
	from_postID="null"
	from_number=0
	let nb_of_users--;
	fi;
}

FILENAME=${1}
nb_of_users=0
#MAX_POSTS=300 Most users does not even have 100 posts...
NB_POSTS=100 # Max that can be return by reddit API

out_of_date_users=""

while read LINE
do
	username=${LINE} 
	from_postID=""
	from_number=0
    let nb_of_users++
    
    while [[ "${from_postID}" != "null" ]]
    do
    getJSON
    sleep '2' #In order not to 'kill reddit'
    done
    echo -e "${nb_of_users}. Fetched <= ${from_number} posts from user ${username}."
done < "${FILENAME}"

echo -e "\nTotal $nb_of_users users fetched. These users are not public anymore: ${out_of_date_users}"





