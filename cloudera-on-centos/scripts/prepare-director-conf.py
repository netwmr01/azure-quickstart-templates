from pyhocon import ConfigFactory
from pyhocon import tool
import sys


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




conf = ConfigFactory.parse_file('/Users/mwei/Documents/azure.simple.conf')
name = sys.argv[1]
region = sys.argv[2]
subscriptionId = sys.argv[3]
tenantId = sys.argv[4]
clientId = sys.argv[5]
clientSecret = sys.argv[6]

username = sys.argv[7]
privateKey = sys.argv[8]

networkSecuritGroupResourceGroup = sys.argv[9]
networkSecurityGroup = sys.argv[10]
virtualNetworkResourceGroup = sys.argv[11]
virtualNetwork = sys.argv[12]
subnetName = sys.argv[13]
computeResourceGroup = sys.argv[14]
hostFqdnSuffix = sys.argv[15]

dbHostOrIP = sys.argv[16]
dbUserName = sys.argv[17]
dbPassword = sys.argv[18]

masterType = sys.argv[19]
workerType = sys.argv[20]
edgeType = sys.argv[21]

conf.put('name', name)

conf.put('provider.region', region)
conf.put('provider.subscriptionId', subscriptionId)
conf.put('provider.tenantId', tenantId)
conf.put('provider.clientId', clientId)
conf.put('provider.clientSecret', clientSecret)

conf.put('ssh.username', username)
conf.put('ssh.privateKey', privateKey)

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
