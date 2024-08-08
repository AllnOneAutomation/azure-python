import logging
from azure.identity import InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def main():
    try:
        logging.info("Acquiring credentials...")
        # Use this for development environments where you can interact with a browser
        credentials = InteractiveBrowserCredential()
        
        logging.info("Requesting subscription ID from user...")
        subscription_id = input("Please enter subscription id: ")

        logging.info("Creating ResourceManagementClient...")
        resource_mgmt_client = ResourceManagementClient(credentials, subscription_id)
        
        logging.info("Listing resource groups...")
        rsg = list(resource_mgmt_client.resource_groups.list())

        if rsg:
            for r in rsg:
                print(f"Resource Group found: {r.name}")
        else:
            print("No Resource Groups found.")

    except AzureError as e:
        logging.error(f"An Azure error occurred: {e}")
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    logging.info("Script execution completed.")

main()
