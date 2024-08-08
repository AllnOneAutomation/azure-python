from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

credentials = DefaultAzureCredential()

subscription_id = '3873bc09-ef2c-4890-abed-d3a2a70c5cd5'

resource_mgmt_client = ResourceManagementClient(credentials, subscription_id)

resource_group = resource_mgmt_client.resource_groups.list()

resource_list = list(resource_mgmt_client.resources.list())

api_version = '2020-06-01'  # Replace with the correct API version for your resources

for rsg in resource_group:
    for resource in resource_list:
        print(f"Deleting resource {resource.name}...")
        delete_resource =  resource_mgmt_client.resources.begin_delete_by_id(resource.id, api_version)
        print(f"Resource {resource.name} deleted successfully from {resource_group.name}")


