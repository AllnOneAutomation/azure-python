import requests

request = requests.get("https://api.github.com/repos/kubernetes/kubernetes/pulls")

git_details = request.json()

pull_request = {}

for i in git_details:

    owner = i["user"]["login"]

    if owner in pull_request:
        pull_request[owner] += 1
        #pull_request[owner] = pull_request[owner] + 1

    else:
        pull_request[owner] = 1

for owner, count in pull_request.items():
    print(f"{owner} has {count} pull requests")