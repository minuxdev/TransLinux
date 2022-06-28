#!/bin/bash

[ ! -z "$1" ] && DIR="$1" || { echo "Directory: " read -r DIR; }

cd "$DIR";

for file in *;
do
    newName="$(echo "$file" | iconv -t 'ascii//TRANSLIT')"
    # echo "$newName"
    mv -v "$file" "$newName"
done

printf "Done!"
