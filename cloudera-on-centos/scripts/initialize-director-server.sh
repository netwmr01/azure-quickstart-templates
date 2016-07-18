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
log() {
  echo "$(date): [${execname}] $@" >> /tmp/initialize-cloudera-server.log
}

log "initializing Director Server..."

# Disable the need for a tty when running sudo and allow passwordless sudo for the admin user
sed -i '/Defaults[[:space:]]\+!*requiretty/s/^/#/' /etc/sudoers
echo "$ADMINUSER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# mount log device for director server
bash ./prepare-director-disks.sh

log "Set cloudera-manager.repo to CM v5"
yum clean all >> /tmp/initialize-cloudera-server.log

sudo wget http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/cloudera-manager.repo -O /etc/yum.repos.d/cloudera-manager.repo >> /tmp/initialize-cloudera-server.log
sudo wget http://archive.cloudera.com/director/redhat/6/x86_64/director/cloudera-director.repo -O /etc/yum.repos.d/cloudera-director.repo >> /tmp/initialize-cloudera-server.log
# this often fails so adding retry logic
n=0
until [ $n -ge 5 ]
do
    sudo yum install -y oracle-j2sdk* cloudera-director-server cloudera-director-client >> /tmp/initialize-cloudera-director.log 2>> /tmp/initialize-cloudera-director.err && break
    n=$[$n+1]
    sleep 15s
done
if [ $n -ge 5 ]; then log "scp error $remote, exiting..." & exit 1; fi

sudo service cloudera-director-server start
sudo service iptables save
sudo chkconfig iptables off
sudo service iptables stop

