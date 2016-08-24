#!/bin/bash
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This script will walk you through setting up BIND on the host and making the changes needed in
# Azure portal.
#

#
# WARNING
#
# - This script only creates one zone file which supports <= 255 hosts. It has not been tested
#   with > 255 hosts trying to use the same zone file. It "might just work", or it may require
#   manually configuring additional zone files in `/etc/named/named.conf.local` and
#   `/etc/named/zones/`.
# - It is assumed that the Azure nameserver IP address will always be `168.63.129.16`. See more
#   info: https://blogs.msdn.microsoft.com/mast/2015/05/18/what-is-the-ip-address-168-63-129-16/.
#

log() {
  echo "$(date): [${execname}] $@" >> /tmp/initialize-mysql-server.log
}

ADMINUSER=$1
INTERNAL_FQDN_SUFFIX=$2
HOST_IP=$3

log "initializing DNS Server..."

# Disable the need for a tty when running sudo and allow passwordless sudo for the admin user
sed -i '/Defaults[[:space:]]\+!*requiretty/s/^/#/' /etc/sudoers
echo "$ADMINUSER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

sudo yum install mysql-server
sudo service mysqld stop
sudo /sbin/chkconfig mysqld on
sudo service mysqld start 




log "Everything is working!"
exit 0
