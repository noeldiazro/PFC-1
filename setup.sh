#!/bin/bash

#													#
#		INSTALLS ALL SOFTWARE DEPENDENCIES			#
#	  tested in a fresh raspbian setup via NOOBS	#
#													#

sudo apt-get update
sudo apt-get install -y python-wxtools python-matplotlib git
echo "Installing now piDA lib..."
cd /tmp/
git clone https://github.com/noeldiazro/pida.git
cd ./pida
./setup.sh --no-update
cd
echo "Cleaning up..."
sudo rm -r /tmp/pida
