import requests

url = 'http://127.0.0.1:5000'

params = {'username': 'cisco', "password": "cisco"}
x = requests.post(url + '/auth', json = params)
utoken = x.json().get('token')
print("utoken: %s"%utoken)

params = {'username': 'hacker', "password": "cisco"}
x = requests.post(url + '/auth', json = params)
atoken = x.json().get('token')
print("atoken: %s"%atoken)

x = requests.post(url + '/create-card', headers={'Authorization': atoken})
print(x.text)

# params = {'id': '3'}
# x = requests.get(url + '/get-card', params = params, headers={'Authorization': atoken})
# print(x.text)


# curl -X POST http://127.0.0.1:5000 -H 'Content-Type: application/json' -d '{"username":"cisco","password":"cisco"}'