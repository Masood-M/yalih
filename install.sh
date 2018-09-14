#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

cd /opt

#apt-get update

apt-get install -y nano python nano git make g++ autoconf automake libtool python-dev libpcre3-dev flex bison python-setuptools python-lxml

wget https://bootstrap.pypa.io/get-pip.py

python get-pip.py

yes | git clone https://github.com/Masood-M/yalih.git

cd yalih

cd jsbeautifier

python setup.py build

python setup.py install



cd /opt/yalih/

cd req

tar -xzvf yara-2.0.0.tar.gz

cd yara-2.0.0

sudo sh build.sh

sudo make install



cd yara-python

python setup.py build

python setup.py install

echo "/usr/local/lib" >> /etc/ld.so.conf

ldconfig


pip install python-magic

pip install psutil

pip install tldextract

pip install mechanize
