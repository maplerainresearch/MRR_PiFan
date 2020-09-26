#! /bin/sh

set -e

echo "-> Installing required libraries...\n"
pip3 install -r requirements.txt

echo "=> Installing fan controller...\n"
sudo cp fancontrol.py /usr/local/bin/
sudo chmod +x /usr/local/bin/fancontrol.py

echo "=> Starting fan controller...\n"
sudo cp fancontrol.sh /etc/init.d/
sudo chmod +x /etc/init.d/fancontrol.sh

sudo update-rc.d fancontrol.sh defaults
sudo /etc/init.d/fancontrol.sh start

echo "Fan controller installed."