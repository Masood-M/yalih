#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

cd /opt

apt-get update

apt-get install -y nano python nano git make gcc g++ autoconf automake libtool python-dev libpcre3-dev flex bison python-setuptools python-lxml libelf-dev

wget https://bootstrap.pypa.io/get-pip.py

python get-pip.py

#yes | git clone https://github.com/Masood-M/yalih.git

cd yalih
cd jsbeautifier
python setup.py build
python setup.py install



cd /opt/yalih/

cd req
#wget https://github.com/VirusTotal/yara/archive/v3.8.1.tar.gz
tar -xzvf v3.9.0.tar.gz

cd /opt/yalih/req/yara-3.9.0/
sudo bash bootstrap.sh
sudo ./configure
sudo make
sudo make install



sudo echo "/usr/local/lib" >> /etc/ld.so.conf
ldconfig


sudo pip install python-magic
sudo pip install psutil
sudo pip install tldextract
sudo pip install mechanize

