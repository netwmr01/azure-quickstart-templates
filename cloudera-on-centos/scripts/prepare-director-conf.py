from pyhocon import ConfigFactory
from pyhocon import ConfigTree
from pyhocon import tool
import sys


def setInstanceParameters (section, networkSecurityGroupResourceGroup, networkSecurityGroup, subnetName,
                           computeResourceGroup, hostFqdnSuffix):
  conf.put(section+'.networkSecuritGroupResourceGroup', networkSecurityGroupResourceGroup)
  conf.put(section+'.networkSecurityGroup', networkSecurityGroup)




conf = ConfigFactory.parse_file('/Users/mwei/Documents/azure.simple.conf')
name = sys.argv[1]
region = sys.argv[2]
subscriptionId = sys.argv[3]
tenantId = sys.argv[4]
clientId = sys.argv[5]
clientSercret = sys.argv[6]

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

subscriptionId = conf.get('provider.subscriptionId')
print subscriptionId
conf.put('name', name)

conf.put('provider.region', region)
conf.put('provider.subscriptionId', subscriptionId)
conf.put('provider.tenantId', tenantId)
conf.put('provider.clientId', clientId)
conf.put('provider.clientSecret', clientSercret)

conf.put('ssh.username', username)
conf.put('ssh.privateKey', privateKey)

conf.put('instances.ds14-master.type', masterType)
conf.put('instances.ds14-worker.type', workerType)
conf.put('instances.ds14-edge.type', edgeType)

conf.put('databaseServers.mysqlprod1.host', dbHostOrIP)
conf.put('databaseServers.mysqlprod1.user', dbUserName)
conf.put('databaseServers.mysqlprod1.password', dbPassword)

print tool.HOCONConverter.to_hocon(conf)
