#!/bin/bash

#get the .json of the user
getJSON()
{
	
	if [ ${from_number} -gt 0 ]; then
	data=`curl -s "http://www.reddit.com/user/${LINE}/liked/.json?limit=${NB_POSTS}&after=${from_postID}&count=${from_number}"`
	else
	data=`curl -s "http://www.reddit.com/user/${LINE}/liked/.json?limit=${NB_POSTS}"`
	fi;
	
	let from_number+=${NB_POSTS}
	
	#get the id of the next post.
	from_postID=`echo ${data} | sed -E 's/.*\"after\":.\"?([^\".]*)\"?,.*/\1/'`
	
	regex='t3_.*'
	
	#In case of 404...
	if [ "${from_postID}" = "{error: 404}" ]; then
		from_postID="null"
		from_number=0
		let nb_private_users++
		echo -e "${username}" >> "private_users.txt";
	elif [[ ${from_postID} =~ $regex || "${from_postID}" = "null" ]]; then 
		if [ ${from_number} -eq "100" ]; then 
		echo -e "${username}" >> "public_users.txt"
		fi
		if [ "${METHOD}" = "check" ]; then
			from_postID="null"
		else
			echo ${data} > "$PWD/json/TEST-${LINE}-${from_number}.json";
		fi	
	else 
		echo -e "${username}" >> "error_users.txt"
		echo -e "error on user ${username}: \n ${from_postID}"
		from_postID="null";
	fi
}

METHOD=""
if [ "$#" -gt "0" ]; then
	FILENAME=${1}
	if [ "$#" -eq "2" ]; then
		METHOD=${2};
	fi
else 
	echo "Use: ./fetch.sh filename [check]"
	exit -1
fi


if [ ! -d "json" ]; then
    mkdir "json"
    echo "created a folder named json"
fi
	
nb_of_users=0
#MAX_POSTS=300 Most users does not even have 100 posts...
NB_POSTS=100 # Max that can be return by reddit API

if [ "${METHOD}" = "check" ]; then
	NB_POSTS=1;
fi

nb_private_users=0

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
    nb_public_users=`expr ${nb_of_users} - ${nb_private_users}`
    echo -e "${nb_of_users}. Fetched <= ${from_number} posts from user ${username}."
done < "${FILENAME}"

echo -e "\nTotal $nb_of_users users fetched. (${nb_public_users} public and ${nb_private_users} private users)"





