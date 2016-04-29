import requests


payload = 'username=patricksong&password=1973Simona'
headers = {'X-Application': '3bU0BLQyEKubZTh3', 'Content-Type': 'application/x-www-form-urlencoded'}

resp = requests.post('https://identitysso.betfair.com/api/certlogin', data=payload, cert=('client-2048.crt', 'client-2048.key'), headers=headers)

if resp.status_code == 200:
  resp_json = resp.json()
  print resp_json['loginStatus']
  print resp_json['sessionToken']
else:
  print "Request failed."