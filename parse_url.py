import os

import requests

url = 'https://medium.com/@mrkaran/my-experience-at-cloud-hack-e8874e0e97f9'

parse_url = 'https://mercury.postlight.com/parser?url=' + url

api_key = os.environ['mercury_api_key']
r = requests.get(parse_url, headers={'x-api-key': api_key}).json()

print(r)
print(r['content'])
