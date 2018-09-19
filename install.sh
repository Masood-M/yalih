#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

cd /opt

#apt-get update

apt-get install -y nano python nano git make gcc g++ autoconf automake libtool python-dev libpcre3-dev flex bison python-setuptools python-lxml

wget https://bootstrap.pypa.io/get-pip.py

python get-pip.py

yes | git clone https://github.com/Masood-M/yalih.git

cd yalih

cd jsbeautifier

python setup.py build

python setup.py install



cd /opt/yalih/

cd req
wget https://github.com/VirusTotal/yara/archive/v3.8.1.tar.gz
tar -xzvf v3.8.1.tar.gz

cd yara-3.8.1/
./configure
sudo make
sudo make install



cd /opt/yalih/

cd yara-python

python setup.py build

python setup.py install

echo "/usr/local/lib" >> /etc/ld.so.conf

ldconfig


pip install python-magic

pip install psutil

pip install tldextract

pip install mechanize


#install antiviruses and update them
cd /opt/
sudo wget https://cdn.download.comodo.com/cis/download/installs/linux/cav-linux_x86.deb
sudo dpkg -i cav-linux_x86.deb

sudo apt-get install clamav
sudo freshclam
sudo /opt/COMODO/cavupdater
###end of antivirus installations

