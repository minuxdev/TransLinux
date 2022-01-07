#!/bin/bash

echo "Directory: "
read DIR

cd "$DIR"; ls

for file in *;
do
newname=`echo "$file" | iconv -t 'ascii//TRANSLIT'`

echo $newname

mv -v "$file" "$newname"

ls $DIR

done
