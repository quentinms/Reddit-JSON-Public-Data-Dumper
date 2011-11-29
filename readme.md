#Reddit JSON Public Data Dumper

It's a simple bash script that downloads the .json of liked from every public user of a file.

If there is more than 100 liked, it sends another request to get the following 100 likes.

####Use:
chmod u+x fetch.sh  
./fetch.sh userlist.txt 

####Todo:
Handle dislikes also.