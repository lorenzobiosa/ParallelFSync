#!/bin/bash

SOURCE=$(grep SOURCE config.py | awk '{ print $NF }' | tr -d '"')
DEST=$(grep DEST config.py | awk '{ print $NF }' | tr -d '"')

python3 scanner.py

cp file_list.txt file_list_new.txt
sed -i "s|${SOURCE}|${DEST}|g" file_list_new.txt
paste -d',' file_list.txt file_list_new.txt > files.txt

rsync -a -f"+ */" -f"- *" ${SOURCE}/* ${DEST}

python3 syncer.py
