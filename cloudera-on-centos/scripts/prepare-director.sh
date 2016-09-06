#!/usr/bin/env bash

name = ${1}
region = ${2}
subscriptionId = ${3}
tenantId = ${4}
clientId = ${5}
clientSecret = ${6}

username = ${7}
passphrase = ${8}
privateKey = ${9}

networkSecuritGroupResourceGroup = ${10}
networkSecurityGroup = ${11}
virtualNetworkResourceGroup = ${12}
virtualNetwork = ${13}
subnetName = ${14}
computeResourceGroup = ${15}
hostFqdnSuffix = ${16}

dbHostOrIP = ${17}
dbUserName = ${18}
dbPassword = ${19}

masterType = ${20}
workerType = ${21}
edgeType = ${22}
dirUsername = ${23}
dirPassword = ${24}

python prepare-director-conf.py ${name} ${region} ${subscriptionId} ${tenantId} ${clientId} ${clientSecret} ${username} \
${passphrase} ${privateKey} ${networkSecuritGroupResourceGroup} ${networkSecurityGroup} ${virtualNetworkResourceGroup} \
${virtualNetwork} ${subnetName} ${computeResourceGroup} ${hostFqdnSuffix} ${dbHostOrIP} ${dbUserName} ${dbPassword} \
${masterType} ${workerType} ${edgeType} ${dirUsername} ${dirPassword}

python setup-default.py --admin-username ${dirUsername} --admin-password ${dirPassword} "/tmp/azure.conf"

exit 0