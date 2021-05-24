#!/bin/sh -l
echo "Attempting to run the update"
echo $1
echo "adding quotes"
echo \"$1\" > modified_files.txt
echo here
python sample_TSC.py