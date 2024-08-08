from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

credentials = DefaultAzureCredential()

subscription_id = '3873bc09-ef2c-4890-abed-d3a2a70c5cd5'


resource_mgmt_client = ResourceManagementClient(credentials, subscription_id)

rsg_parameter =  {"location": "eastus"}

resource_mgmt_client.resource_groups.create_or_update("myResourceGroup", rsg_parameter)

# You can find the API version in the Azure documentation or by examining the resource properties in the Azure portal.
api_version = '2020-06-01'  # Replace with the correct API version for your resources

for rsg in resource_mgmt_client.resource_groups.list():
    if rsg.name == "myResourceGroup":
        print (f"{rsg.name} Resource Group found")
    
        #adding tags to the rsg myResourceGroup
        rsg_parameter.update(tags={"Environment": "Test"})
        resource_mgmt_client.resource_groups.update(rsg.name, rsg_parameter)
        print("Tags added successfully")

        #finding resources in the rsg myResourceGroup
        resource_list = list(resource_mgmt_client.resources.list_by_resource_group(rsg.name))
       
        if resource_list:
            for resource in resource_list:
                print(f"Deleting resource {resource.name} from {rsg.name}...")
                delete_resource =  resource_mgmt_client.resources.begin_delete_by_id(resource.id, api_version)
        else:
                print(f"No resources found in the resource group {rsg.name}")

                
            
        #delete_rsg = resource_mgmt_client.resource_groups.begin_delete(rsg.name)
        #print(f"Deleting Resource Group {rsg.name}...")

    else:
        print(f"Resource Group not found")
    