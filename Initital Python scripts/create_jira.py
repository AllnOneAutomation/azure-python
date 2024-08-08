# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://arshanmulla.atlassian.net/rest/api/3/issue"

auth = HTTPBasicAuth("arshanmulla13@gmail.com", "ATATT3xFfGF0Hu7U2GYOVmqLotoCVUxK3bdc9W0KyqEh9-IS16rNdp0CnzqvVz0yAxkHfaVTxSJ9ASjcrcip7j9g3Jwyi2IKClTYBzMoF9Tq0u9sRYrYKWP7rNNVjcYNlkFZizjRGKb3gsFvNJtcxDviSYsvLUjPhc2O9f3I2cY8dxHnUZjcrl8=47F3C8AA")

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "fields": {
    "description": {
      "content": [
        {
          "content": [
            {
              "text": "My first jira ticket",
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    "project": {
      "key": "SCRUM"
    },
    "issuetype": {
      "id": "10003"
    },
    "summary": "First JIRA Ticket",
  },
  "update": {}
} )

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))