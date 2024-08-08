# app-1.py
from flask import Flask, render_template, request
from azure_vm_rdp_disabler import disable_rdp
from azure_vm_disable_https import disable_https
from azure.identity import ClientSecretCredential
from azure.core.exceptions import AzureError


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/apply_settings', methods=['POST'])
def apply_settings():
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']
    tenant_id = request.form['tenant_id']
    vm_name = request.form['vm_name']
    subscription_id = request.form['subscription_id']
    resource_group_name = request.form['resource_group_name']
    settings = request.form.getlist('settings')  # Get selected settings

    print(f"client_id: {client_id}")
    print(f"client_secret: {client_secret}")
    print(f"tenant_id: {tenant_id}")
    print(f"vm_name: {vm_name}")
    print(f"subscription_id: {subscription_id}")
    print(f"resource_group_name: {resource_group_name}")

    if not client_id or not client_secret or not tenant_id:
        return "Please provide valid Azure credentials"

    try:
        # Use ClientSecretCredential to authenticate
        credential = ClientSecretCredential(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id
        )

        # Authenticate with Azure
        token = credential.get_token("https://management.azure.com/.default")
    except AzureError as e:
        return f"Authentication failed: {str(e)}"

    if 'disablerdp' in settings:
        rdp_result = disable_rdp(vm_name, subscription_id, resource_group_name, client_id, client_secret, tenant_id)
        if "Success" in rdp_result:
            return f"RDP disabled successfully: {rdp_result}"
        else:
            return f"Failed to disable RDP: {rdp_result}"

    if 'disablehttps' in settings:
        https_result = disable_https(vm_name, subscription_id, resource_group_name, client_id, client_secret, tenant_id)
        if https_result == "Success":
            return f"HTTPS disabled successfully: {https_result}"
        else:
            return f"Failed to disable HTTPS: {https_result}"

    return "No settings selected"

if __name__ == '__main__':
    app.run(debug=True)
