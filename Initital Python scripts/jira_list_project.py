# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests #used to make api calls
from requests.auth import HTTPBasicAuth #authentication with Jira
import json 
 
url = "https://arshanmulla.atlassian.net/rest/api/3/project"

auth = HTTPBasicAuth("arshanmulla13@gmail.com", "ATATT3xFfGF0Hu7U2GYOVmqLotoCVUxK3bdc9W0KyqEh9-IS16rNdp0CnzqvVz0yAxkHfaVTxSJ9ASjcrcip7j9g3Jwyi2IKClTYBzMoF9Tq0u9sRYrYKWP7rNNVjcYNlkFZizjRGKb3gsFvNJtcxDviSYsvLUjPhc2O9f3I2cY8dxHnUZjcrl8=47F3C8AA")

headers = {
  "Accept": "application/json"
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


# output = json.loads(response.text)

# project_name = output[0]["name"]

# print(project_name)