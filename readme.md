#Reddit JSON Public Data Dumper

It's a simple bash script that downloads the .json of liked from every public user of a file.

If there is more than 100 liked, it sends another request to get the following 100 likes.

>> Now in Python! \o/ <<

####Use:
chmod u+x fetch.sh  
./fetch.sh userlist.txt [check]

The optional check argument will result in outputting only a text file of public users and a text file of private users and no .json files.

####Todo:
Handle dislikes also.