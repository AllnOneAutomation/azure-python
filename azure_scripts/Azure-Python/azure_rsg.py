from azure.identity import DefaultAzureCredential #import the DefaultAzureCredential class from the azure.identity module
from azure.mgmt.resource import ResourceManagementClient #import the ResourceManagementClient class from the azure.mgmt.resource module

credentials = DefaultAzureCredential()  #create an instance of DefaultAzureCredential
subscription_id = '3873bc09-ef2c-4890-abed-d3a2a70c5cd5' 
resource_mgmt_client = ResourceManagementClient(credentials, subscription_id) #create an instance of ResourceManagementClient


def rsg_list():
    # Get a list of all resource groups in the subscription
    resource_group_list = resource_mgmt_client.resource_groups.list() #list method to get a list of all resource groups in the subscription
    # Iterate over the list of resource groups
    for resource_group in resource_group_list:
        # Get a list of all resources in the current resource group
        resources_in_group = list(resource_mgmt_client.resources.list_by_resource_group(resource_group.name))     #list_by_resource_group method to get a list of all resources in a resource group
        # Check if the list of resources in the group is not empty
        if resources_in_group:
            print(f"There are some resources in the resource group '{resource_group.name}'.")
        else:
            print(f"There are no resources in the resource group '{resource_group.name}'.")

# Call the function to list resources in each resource group
rsg_list()