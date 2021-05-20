import requests
import json
from log import MyLogger

logger = MyLogger(log_file='logs.log', log_path='logs', name=__name__)

url = "https://10ax.online.tableau.com/api/3.11/auth/signin"


# For Tableau Server, if a sign in request body is missing a site element, is missing 
# the contentUrl attribute, or contains a contentUrl whose value is an empty string,
# then the result is identical to specifying the Default site as the contentUrl.
# For Tableau Online, a site element containing a contentUrl with the value of an
# existing site must always be provided. If these are missing, the Sign In 
# request will fail.


payload = json.dumps({
  "credentials": {
    "site": {
      "contentUrl": "dsmdaviddev799594"
    },
    "personalAccessTokenName": "dvd-test",
    "personalAccessTokenSecret": "JE5h4Vg6QG6BlULks0F5SQ==:I72UGbMZPbMDk5jYVaD33SrDgN9Kn15m"
  }
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
  }

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
