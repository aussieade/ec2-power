#!/bin/bash
# 
# Filename: ec2-power.sh
# Version: 0.1.0
# Author: Ade
# Description: cloud-init example script to setup ec2-power
# 

# Change Log:
# 

LOCATION=http://wherever.you.put/ec2-power.py
OPERATOR=/home/ec2-user/ec2-power.py

yum install -y python-pip gcc
pip install croniter
wget -O $OPERATOR $LOCATION
chown ec2-user:ec2-user $OPERATOR
chmod 644 $OPERATOR
#echo '*/5 * * * * ec2-user python $OPERATOR >>/home/ec2-user/ec2-power.log 2>&1' >> /etc/crontab
