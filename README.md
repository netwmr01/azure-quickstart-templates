# Azure (ARM) templates for deploying long running clusters (non-Director managed)

There are 2 main branches for this repo:

1. master: This is the "github" version of the quickstart templates.
1. ui: This is the Azure Marketplace UI version of the quickstart templates.

github version is the basis of the Marketplace UI version. The 2 are mostly identical. The UI version contains some UI definitions and certain files might be named differently.

## Work flow
1. Checkout master (make a feature branch in order to do PR) and implement changes against master. NOTE: We will be working against the ```strata_mvp``` & ```strata_mvp_ui``` branches in the next few weeks.
1. Send PR against master.
1. Commit changes after getting +1 from review to master branch.
1. Checkout ui branch (make a feature branch in order to do PR) and cherry-pick changes from master to ui (feature) branch.
1. Send PR against ui branch.
1. Commit changes after getting +1 from review to ui branch.

### NOTE:
If making UI only changes, just start from step 4 above.

## Test flow
Testing the Azure Marketplace templates **requires the templates to be reachable over the public internet by Azure**. This is not possible when all the code is hosted on Cloudera's github instance. What we will do for now is use Mingrui's public github for testing. The following are the detailed steps:

1. Follow the Work flow section above to do code changes and reviews.
1. Checkout Mingrui's repo by ```git clone git@github.com:netwmr01/azure-quickstart-templates.git``` NOTE: This uses your public github credentials.
1. Checkout a new branch and delete everything in it.
1. Copy the templates you are working on to this new branch.
1. Commit the change locally.
1. Modify the ```azuredeploy.json``` file by updating ```scriptsUri``` field to point to the raw file link to your own branch. eg. ```https://raw.githubusercontent.com/netwmr01/azure-quickstart-templates/your_branch_name/your_template_folder```
1. Modify the ```README.md``` file to point the "Deploy on Azure" link to your own branch like the earlier step. eg. ```<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnetwmr01%2Fazure-quickstart-templates%2Fname_of_your_branch%2Fname_of_your_template_dir%2Fazuredeploy.json" target="_blank">```
1. Commit change locally and push to remote.
1. You can then test by clicking the "Deploy on Azure" button from the README.md file in your branch on github.com.

Alternatively you can test by Azure CLI:

1. Create a resource group: ```azure group create -n ExampleResourceGroupEast -l "East US"```
1. Deploy template using a set of params: ```azure group deployment create -f azuredeploy.json -e azuredeploy.parameters.json -g ExampleResourceGroupEast -n ExampleDeploymentEast``` . NOTE: You Parameter file will contain sensitive subscription info, Do **NOT** commit your parameter file should not be committed to public or internal github.
1. Delete the resource group: ```echo "y" | azure group delete ExampleResourceGroupEast```

### NOTE:

* You should iterate (trial & error) your changes on the external github repo, which will reduce the hassle of bring changes back and forth between internal and external repos.
* When you are done, delete the **remote** branch.
* The reason to do this copying to a new repo thing is to make sure we don't accidentally dump a bunch of commit history with internal JIRA IDs to github.com . This is a bit painful and we should try to make this simpler if possible.