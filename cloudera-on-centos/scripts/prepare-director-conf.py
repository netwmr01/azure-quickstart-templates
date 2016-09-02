from pyhocon import ConfigFactory
from pyhocon import tool
import sys
import logging
from subprocess import call
call(["ls", "-l"])

logging.basicConfig(filename='/tmp/prepare-director-conf.log', level=logging.DEBUG)
logging.info('started')

def setInstanceParameters (section, machineType, networkSecurityGroupResourceGroup, networkSecurityGroup, virtualNetworkResourceGroup,
                           virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix):
  conf.put(section+'.type', machineType)
  conf.put(section+'.networkSecurityGroupResourceGroup', networkSecurityGroupResourceGroup)
  conf.put(section+'.networkSecurityGroup', networkSecurityGroup)
  conf.put(section+'.virtualNetworkResourceGroup', virtualNetworkResourceGroup)
  conf.put(section+'.virtualNetwork', virtualNetwork)
  conf.put(section+'.subnetName', subnetName)
  conf.put(section+'.computeResourceGroup', computeResourceGroup)
  conf.put(section+'.hostFqdnSuffix', hostFqdnSuffix)

def writeToFile(privateKey, keyFileName):
  target = open(keyFileName, 'w')
  target.truncate()
  target.write(privateKey)
  target.close()


conf = ConfigFactory.parse_file('/tmp/azure.simple.conf')
name = sys.argv[1]
region = sys.argv[2]
subscriptionId = sys.argv[3]
tenantId = sys.argv[4]
clientId = sys.argv[5]
clientSecret = sys.argv[6]

username = sys.argv[7]
passphrase = sys.argv[8]
privateKey = sys.argv[9]
keyFileName = "/tmp/keyfile"
writeToFile(privateKey, keyFileName)

networkSecuritGroupResourceGroup = sys.argv[10]
networkSecurityGroup = sys.argv[11]
virtualNetworkResourceGroup = sys.argv[12]
virtualNetwork = sys.argv[13]
subnetName = sys.argv[14]
computeResourceGroup = sys.argv[15]
hostFqdnSuffix = sys.argv[16]

dbHostOrIP = sys.argv[17]
dbUserName = sys.argv[18]
dbPassword = sys.argv[19]

masterType = sys.argv[20]
workerType = sys.argv[21]
edgeType = sys.argv[22]

conf.put('name', name)

conf.put('provider.region', region)
conf.put('provider.subscriptionId', subscriptionId)
conf.put('provider.tenantId', tenantId)
conf.put('provider.clientId', clientId)
conf.put('provider.clientSecret', clientSecret)

conf.put('ssh.username', username)
if passphrase:
  conf.put('ssh.passphrase', passphrase)
conf.put('ssh.privateKey', keyFileName)


setInstanceParameters('instances.ds14-master', masterType, networkSecuritGroupResourceGroup, networkSecurityGroup,
                      virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
setInstanceParameters('instances.ds14-worker', workerType, networkSecuritGroupResourceGroup, networkSecurityGroup,
                      virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
setInstanceParameters('instances.ds14-edge', edgeType, networkSecuritGroupResourceGroup, networkSecurityGroup,
                      virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
setInstanceParameters('cloudera-manager.instance', edgeType, networkSecuritGroupResourceGroup, networkSecurityGroup,
                      virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
setInstanceParameters('cluster.masters.instance', masterType, networkSecuritGroupResourceGroup, networkSecurityGroup,
                      virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
setInstanceParameters('cluster.workers.instance', masterType, networkSecuritGroupResourceGroup, networkSecurityGroup,
                      virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)

conf.put('databaseServers.mysqlprod1.host', dbHostOrIP)
conf.put('databaseServers.mysqlprod1.user', dbUserName)
conf.put('databaseServers.mysqlprod1.password', dbPassword)

with open("/tmp/azure.conf", "w") as text_file:
    text_file.write(tool.HOCONConverter.to_hocon(conf))

logging.info('finish')
