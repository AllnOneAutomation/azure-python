from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


credentials = DefaultAzureCredential()
subscription_id = '3873bc09-ef2c-4890-abed-d3a2a70c5cd5'

resource_mgmt_client = ResourceManagementClient(credentials, subscription_id)
rsg = list(resource_mgmt_client.resource_groups.list())

for r in rsg:
    if r:
        print (f"Resource Group found {r.name}")

    else:
        print ("Resource Group not found")