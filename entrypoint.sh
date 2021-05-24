#!/bin/sh -l
echo "Attempting to run the update"
echo $1
echo "adding quotes"
echo \"$1\"
$1
python sample_TSC.py --modified \"$1\"