from pyhocon import ConfigFactory
from pyhocon import tool
import os
import logging
import sys
from optparse import OptionParser

# logging starts
logging.basicConfig(filename='/tmp/prepare-director-conf.log', level=logging.DEBUG)
logging.info('started')

dirUsername = 'admin'
dirPassword = 'admin'

def parse_options():

    parser = OptionParser()

    parser.add_option('--envName', dest='env', type="string", help='Environment name')
    parser.add_option('--region', dest='region', type="string", help='Set Azure Region')
    parser.add_option('--subId',  dest='subId', type="string", help='Set Azure Subscription ID')
    parser.add_option('--tenantId', dest='tenantId', type="string", help='Set Azure tenant ID')
    parser.add_option('--clientId', dest='clientId', type="string", help='Set Azure client ID')
    parser.add_option('--clientSecret', dest='clientSecret', type="string", help='Set Azure client secret')
    parser.add_option('--username', dest='username', type="string", help='Set key file name')
    parser.add_option('--keyFileName', dest='keyFileName', type="string", help='Set company')
    parser.add_option('--networkSecurityGroupResourceGroup', dest='networkSecurityGroupResourceGroup', type="string",
                      help='Set NetworkSecurityGroup ResourceGroup')
    parser.add_option('--networkSecurityGroup', dest='networkSecurityGroup', type="string", help='Set NetworkSecurityGroup')
    parser.add_option('--virtualNetworkResourceGroup', dest='virtualNetworkResourceGroup', type="string",
                      help='Set virtualNetworkResourceGroup')
    parser.add_option('--virtualNetwork', dest='virtualNetwork', type="string", help='Set virtualNetwork')
    parser.add_option('--subnetName', dest='subnetName', type="string", help='Set subnetName')
    parser.add_option('--computeResourceGroup', dest='computeResourceGroup', type="string", help='Set computeResourceGroup')
    parser.add_option('--hostFqdnSuffix', dest='hostFqdnSuffix', type="string", help='Set hostFqdnSuffix')
    parser.add_option('--dbHostOrIP', dest='dbHostOrIP', type="string", help='Set dbHostOrIP')
    parser.add_option('--dbUsername', dest='dbUsername', type="string", help='Set dbUsername')
    parser.add_option('--dbPassword', dest='dbPassword', type="string", help='Set dbPassword')
    parser.add_option('--masterType', dest='masterType', type="string", help='Set masterType')
    parser.add_option('--workerType', dest='workerType', type="string", help='Set workerType')
    parser.add_option('--edgeType', dest='edgeType', type="string", help='Set edgeType')


    (options, args) = parser.parse_args()

    return options


def setInstanceParameters (conf, section, machineType, networkSecurityGroupResourceGroup, networkSecurityGroup, virtualNetworkResourceGroup,
                           virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix):
  conf.put(section+'.type', machineType)
  conf.put(section+'.networkSecurityGroupResourceGroup', networkSecurityGroupResourceGroup)
  conf.put(section+'.networkSecurityGroup', networkSecurityGroup)
  conf.put(section+'.virtualNetworkResourceGroup', virtualNetworkResourceGroup)
  conf.put(section+'.virtualNetwork', virtualNetwork)
  conf.put(section+'.subnetName', subnetName)
  conf.put(section+'.computeResourceGroup', computeResourceGroup)
  conf.put(section+'.hostFqdnSuffix', hostFqdnSuffix)

def generateKeyToFile(keyFileName):
  command='ssh-keygen -f %s -q -N ""'%(keyFileName)
  os.system(command)

def prepareConf(options):
  conf = ConfigFactory.parse_file('azure.simple.conf')
  logging.info('parsed conf')
  name = options.env
  region = options.region
  subscriptionId = options.subId
  tenantId = options.tenantId
  clientId = options.clientId
  clientSecret = options.clientSecret

  username = options.username
  keyFileName = options.keyFileName
  generateKeyToFile(keyFileName)

  networkSecurityGroupResourceGroup = options.networkSecurityGroupResourceGroup
  networkSecurityGroup = options.networkSecurityGroup
  virtualNetworkResourceGroup = options.virtualNetworkResourceGroup
  virtualNetwork = options.virtualNetwork
  subnetName = options.subnetName
  computeResourceGroup = options.computeResourceGroup
  hostFqdnSuffix = options.hostFqdnSuffix

  dbHostOrIP = options.dbHostOrIP
  dbUsername = options.dbUsername
  dbPassword = options.dbPassword

  masterType = options.masterType
  workerType = options.workerType
  edgeType = options.edgeType

  logging.info('parameters assigned')

  conf.put('name', name)
  conf.put('provider.region', region)
  conf.put('provider.subscriptionId', subscriptionId)
  conf.put('provider.tenantId', tenantId)
  conf.put('provider.clientId', clientId)
  conf.put('provider.clientSecret', clientSecret)

  conf.put('ssh.username', username)
  conf.put('ssh.privateKey', keyFileName)


  setInstanceParameters(conf, 'instances.ds14-master', masterType, networkSecurityGroupResourceGroup, networkSecurityGroup,
                        virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
  setInstanceParameters(conf, 'instances.ds14-worker', workerType, networkSecurityGroupResourceGroup, networkSecurityGroup,
                        virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
  setInstanceParameters(conf, 'instances.ds14-edge', edgeType, networkSecurityGroupResourceGroup, networkSecurityGroup,
                        virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
  setInstanceParameters(conf, 'cloudera-manager.instance', edgeType, networkSecurityGroupResourceGroup, networkSecurityGroup,
                        virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
  setInstanceParameters(conf, 'cluster.masters.instance', masterType, networkSecurityGroupResourceGroup, networkSecurityGroup,
                        virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)
  setInstanceParameters(conf, 'cluster.workers.instance', masterType, networkSecurityGroupResourceGroup, networkSecurityGroup,
                        virtualNetworkResourceGroup, virtualNetwork, subnetName, computeResourceGroup, hostFqdnSuffix)

  conf.put('databaseServers.mysqlprod1.host', dbHostOrIP)
  conf.put('databaseServers.mysqlprod1.user', dbUsername)
  conf.put('databaseServers.mysqlprod1.password', dbPassword)

  logging.info('conf value replaced')

  with open("/tmp/azure.conf", "w") as text_file:
      text_file.write(tool.HOCONConverter.to_hocon(conf))

  logging.info("conf file has been written")

  command="python setup-default.py --admin-username %s --admin-password %s /tmp/azure.conf"%(dirUsername, dirPassword)
  logging.info(command)
  status = os.system(command)
  if status != 0:
    sys.exit(status)
  logging.info('finish')

def main():
    # Parse user options
    logging.info("parse_options")
    options = parse_options()
    prepareConf(options)


if __name__ == "__main__":
    main()
