#!/bin/bash

[ -d "full_songs" ] || mkdir "full_songs"

for file in "$@"
do
    mv "$file" "full_songs/$file"
    sox "full_songs/$file" "${file}_extract.wav" trim 30 30
done
