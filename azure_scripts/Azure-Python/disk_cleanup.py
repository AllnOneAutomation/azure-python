from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

credentials = DefaultAzureCredential()

subscription = input("Please enter subscription id: ")

# Create a ComputeManagementClient object with the provided subscription ID
compute_client = ComputeManagementClient(credentials, subscription)

def disk_cleanup():
  # Get a list of all disks in the subscription
  disks =  compute_client.disks.list()

  # Iterate over the disks
  for disk in disks:
        if not disk.managed_by:
            # If the disk is unattached, delete it
            resource_group_name = disk.id.split("/")[4]
            print(f"Deleting unattached disk {disk.name} in resource group {resource_group_name}...")
            async_delete = compute_client.disks.begin_delete(resource_group_name, disk.name)
            async_delete.result()  # Wait for the delete operation to complete
            print(f"Deleted unattached disk {disk.name}")

        elif disk.managed_by:
            # If the disk is attached, skip it
            print(f"Skipping attached disk {disk.name}")
  else:
    print("No disks found.")

disk_cleanup()