# azure_vm_rdp_disabler.py
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import SecurityRule, NetworkSecurityGroup
from azure.core.exceptions import ResourceNotFoundError
import time

def wait_for_vm_provisioning(compute_client, resource_group_name, vm_name):
    max_retries = 60  # Adjust as needed
    retries = 0

    while retries < max_retries:
        vm = compute_client.virtual_machines.get(resource_group_name, vm_name)
        if vm.provisioning_state == "Succeeded":
            print("VM provisioning completed successfully.")
            return True
        elif vm.provisioning_state == "Failed":
            print("VM provisioning failed.")
            return False

        retries += 1
        time.sleep(5)

    print("Timed out waiting for VM provisioning.")
    return False

def disable_rdp(vm_name, subscription_id, resource_group_name, client_id, client_secret, tenant_id):
    # Create the ClientSecretCredential
    credential = ClientSecretCredential(
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id
    )

    # Create the ComputeManagementClient and NetworkManagementClient
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)

    # Check if the virtual machine exists
    try:
        vm = compute_client.virtual_machines.get(resource_group_name, vm_name)
    except ResourceNotFoundError:
        print(f"Virtual machine '{vm_name}' does not exist in resource group '{resource_group_name}'")
        return f"Virtual machine '{vm_name}' does not exist in resource group '{resource_group_name}'"

    # Check if the virtual machine is connected to a Network Security Group (NSG)
    nic_id = vm.network_profile.network_interfaces[0].id  # Assuming only one network interface is attached

    # Retrieve the NSG ID from the NIC
    nic = network_client.network_interfaces.get(resource_group_name, nic_id.split("/")[-1])
    nsg_id = nic.network_security_group.id if nic.network_security_group else None

    if nsg_id:
        # NSG exists, disable RDP by creating an inbound rule with deny action
        nsg = network_client.network_security_groups.get(resource_group_name, nsg_id.split("/")[-1])
        rule_name = "DisableRDP"
        rdp_rule = None

        # Find the existing "DisableRDP" rule
        for rule in nsg.security_rules:
            if rule.name == rule_name:
                rdp_rule = rule
                break

        if rdp_rule:
            # Update the priority of the existing rule
            rdp_rule.priority = 300
        else:
            # Create a new rule with the updated priority
            rdp_rule = SecurityRule(
                protocol="Tcp",
                source_address_prefix="*",
                source_port_range="*",
                destination_address_prefix="*",
                destination_port_range="3389",
                access="Deny",
                direction="Inbound",
                priority=300,
                name=rule_name
            )
            nsg.security_rules.append(rdp_rule)

        network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg.name, nsg)
        print(f"RDP disabled for VM '{vm_name}' in the existing NSG '{nsg.name}'")
        return f"Success: RDP disabled for VM '{vm_name}' in the existing NSG '{nsg.name}'"

        # Wait for VM provisioning to complete
        if not wait_for_vm_provisioning(compute_client, resource_group_name, vm_name):
            return "Failed to disable RDP: VM provisioning timeout"

    else:
        # NSG does not exist, create a new NSG and disable RDP
        nsg_name = f"{vm_name}-nsg"
        nsg_params = NetworkSecurityGroup(location=vm.location)
        nsg = network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg_name, nsg_params).result()

        rule_name = "DisableRDP"
        rdp_rule = SecurityRule(
            protocol="Tcp",
            source_address_prefix="*",
            source_port_range="*",
            destination_address_prefix="*",
            destination_port_range="3389",
            access="Deny",
            direction="Inbound",
            priority=300,
            name=rule_name
        )

        # Verify NSG creation and wait until it is fully provisioned
        while True:
            nsg = network_client.network_security_groups.get(resource_group_name, nsg.name)
            if nsg.provisioning_state == "Succeeded":
                print("NSG creation completed successfully.")
                break

            # Sleep for a few seconds before checking again
            time.sleep(5)
        nsg.security_rules = [rdp_rule]
        network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg.name, nsg)
        print(f"RDP disabled for VM '{vm_name}' by creating a new NSG '{nsg.name}'")

        # Associate the NSG with the VM's network interface
        nic.network_security_group = nsg
        network_client.network_interfaces.begin_create_or_update(resource_group_name, nic.name, nic)

        # Verify if the NSG is connected to the VM
        vm.network_profile.network_interfaces[0].network_security_group = nsg
        compute_client.virtual_machines.begin_create_or_update(resource_group_name, vm_name, vm)

        # Wait for VM provisioning to complete
        if not wait_for_vm_provisioning(compute_client, resource_group_name, vm_name):
            return "Failed to disable RDP: VM provisioning timeout"

    # Return success message
    return "Success: RDP disabled for VM '{vm_name}' by creating a new NSG '{nsg.name}'"
