# azure_vm_disable_https.py
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import SecurityRule, NetworkSecurityGroup
from azure.core.exceptions import ResourceNotFoundError
import time


def disable_https(vm_name, subscription_id, resource_group_name, client_id, client_secret, tenant_id):
    """
    Disable HTTPS for a virtual machine.

    Args:
        vm_name (str): The name of the virtual machine.
        subscription_id (str): The Azure subscription ID.
        resource_group_name (str): The name of the resource group.
        client_id (str): The client ID for authentication.
        client_secret (str): The client secret for authentication.
        tenant_id (str): The Azure Active Directory tenant ID.
    """
    print(f"client_id: {client_id}")
    print(f"client_secret: {client_secret}")
    print(f"tenant_id: {tenant_id}")
    print(f"vm_name: {vm_name}")
    print(f"subscription_id: {subscription_id}")
    print(f"resource_group_name: {resource_group_name}")

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
        return

    # Check if the virtual machine is connected to a Network Security Group (NSG)
    nic_id = vm.network_profile.network_interfaces[0].id  # Assuming only one network interface is attached
    print(f"nic id is '{nic_id}'")
    # Retrieve the NSG ID from the NIC
    nic = network_client.network_interfaces.get(resource_group_name, nic_id.split("/")[-1])
    print(f"nic is '{nic}'")
    nsg_id = nic.network_security_group.id if nic.network_security_group else None
    print(f"nsg id is '{nsg_id}'")  # Assuming only one network interface is attached
    if nsg_id:
        # NSG exists, disable HTTPS by creating an inbound rule with deny action
        nsg = network_client.network_security_groups.get(resource_group_name, nsg_id.split("/")[-1])
        rule_name = "DisableHTTPS"
        https_rule = None

        # Find the existing "DisableHTTPS" rule
        for rule in nsg.security_rules:
            if rule.name == rule_name:
                https_rule = rule
                break

        if https_rule:
            # Update the priority of the existing rule
            https_rule.priority = 400
        else:
            # Create a new rule with the updated priority
            https_rule = SecurityRule(
                protocol="Tcp",
                source_address_prefix="*",
                source_port_range="*",
                destination_address_prefix="*",
                destination_port_range="443",
                access="Deny",
                direction="Inbound",
                priority=400,
                name=rule_name
            )
            nsg.security_rules.append(https_rule)

        network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg.name, nsg)
        print(f"HTTPS disabled for VM '{vm_name}' in the existing NSG '{nsg.name}'")
    else:
        # NSG does not exist, create a new NSG and disable HTTPS
        nsg_name = f"{vm_name}-nsg"
        nsg_params = NetworkSecurityGroup(location=vm.location)
        nsg = network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg_name,
                                                                            nsg_params).result()

        rule_name = "DisableHTTPS"
        https_rule = SecurityRule(
            protocol="Tcp",
            source_address_prefix="*",
            source_port_range="*",
            destination_address_prefix="*",
            destination_port_range="443",
            access="Deny",
            direction="Inbound",
            priority=400,
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
        nsg.security_rules = [https_rule]
        network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg.name, nsg)
        print(f"HTTPS disabled for VM '{vm_name}' by creating a new NSG '{nsg.name}'")

        # Associate the NSG with the VM's network interface
        nic.network_security_group = nsg
        network_client.network_interfaces.begin_create_or_update(resource_group_name, nic.name, nic)

        # Verify if the NSG is connected to the VM
        vm.network_profile.network_interfaces[0].network_security_group = nsg
        compute_client.virtual_machines.begin_create_or_update(resource_group_name, vm_name, vm)

        # Wait until the VM is fully provisioned
        while True:
            vm = compute_client.virtual_machines.get(resource_group_name, vm_name)
            if vm.provisioning_state == "Succeeded":
                print("VM provisioning completed successfully.")
                break

            # Sleep for a few seconds before checking again
            time.sleep(5)

        # Verify if the NSG is connected to the VM
        nic_id = vm.network_profile.network_interfaces[0].id
        nic = network_client.network_interfaces.get(resource_group_name, nic_id.split("/")[-1])
        nsg_id = nic.network_security_group.id if nic.network_security_group else None

        if nsg_id == nsg.id:
            print(f"NSG '{nsg.name}' is connected to VM '{vm_name}'")
        else:
            print(f"NSG '{nsg.name}' is not connected to VM '{vm_name}'")
