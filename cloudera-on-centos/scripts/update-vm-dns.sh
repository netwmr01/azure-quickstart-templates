#!/usr/bin/env bash

n=120
sleepInterval=10
internal_ip=$1

until [[ ! -z `grep "nameserver ${internal_ip}" /etc/resolv.conf` ]] || [ $n -le 0 ]
do
    service network restart
    echo "Waiting for Azure DNS nameserver updates to propagate, this usually takes less than 2 minutes..."
    n=`expr $n - ${sleepInterval}`
    sleep ${sleepInterval}

done
if [ $n -le 0 ]; then echo  "fail to pick up dns server from vnet" & exit 1; fi