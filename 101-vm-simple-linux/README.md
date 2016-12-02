# azure-template-add-node
This ARM template create a set of worker nodes ready to be added to
existing CDH cluster using CM.

<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnetwmr01%2Fazure-quickstart-templates%2Ftest-bed%2F101-vm-simple-linux%2Fazuredeploy.json" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
</a>
<a href="http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2Fnetwmr01%2Fazure-quickstart-templates%2Ftest-bed%2F101-vm-simple-linux%2Fazuredeploy.json" target="_blank">
    <img src="http://armviz.io/visualizebutton.png"/>
</a>


The template assumes the Virtual Network, Availability Set and Network
Security Group have been created before hand. 

**Resource Naming Pattern**
DNS prefix + copyIndex() is use to create a unique seed for naming
resources to avoid name collisions. 
VirtualMachine name will be prefix-copyIndex()-suffix
StorageAccount will be uniqueString(seed+copyIndex())+"sa"
NetworkInterface will be uniqueString(seed+copyIndex())+"nic"

**Caveat**
1) dns prefix must be unique.
2) dns prefix can be slight different from each other per deployment, 
such as uniquestring1, uniquestring2...