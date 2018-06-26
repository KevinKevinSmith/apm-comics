for isbn in $(cat isbn.txt); do 
	curl -O http://covers.openlibrary.org/b/isbn/$isbn-L.jpg
done
