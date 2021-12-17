import requests
from time import sleep

url = 'http://127.0.0.1:5000'

params = {'username': 'cisco', "password": 'cisco'}
x = requests.post(url + '/auth', json = params)
utoken = x.json().get('token')
uauth = "Bearer " + utoken
print("utoken: %s"%utoken)

sleep(1)
params = {'username': 'hacker', 'password': 'cisco'}
x = requests.post(url + '/auth', json = params)
atoken = x.json().get('token')
aauth = "Bearer " + atoken
print("atoken: %s"%atoken)

sleep(1)

print("\nCreating a card for user cisco using the user token")
x = requests.post(url + '/create-card', json={'username': 'cisco'}, headers={'Authorization': uauth})
card_id1 = x.json().get('id')
print("Response: " + x.text)

sleep(1)

print("\nGetting cards with user token")
x = requests.get(url + '/get-cards', headers={'Authorization': uauth})
print("Response: " + x.text)
print("Expected: 1 card with id %s"%card_id1)

sleep(1)

# print("\nGetting cards with attacker token")
x = requests.get(url + '/get-cards', headers={'Authorization': aauth})
print("Response: " + x.text)
print("Expected: 0 cards")


sleep(1)
print("\nGetting the card with id %s and using the user token"%card_id1)
params = {'id': card_id1}
x = requests.get(url + '/get-card', params=params, headers={'Authorization': uauth})
print("Response: " + x.text)
print("Expected: 1 card with id %s"%card_id1)

sleep(1)

print("\nGetting the card with id %s and using the attacker token"%card_id1)
params = {'id': card_id1}
x = requests.get(url + '/get-card', params=params, headers={'Authorization': aauth})
print("Response: " + x.text)
print("Expected: 0 cards")

sleep(1)

print("\nCreating a card for user cisco using the attacker token")
x = requests.post(url + '/create-card', json={'username': 'cisco'}, headers={'Authorization': aauth})
print("Response: " + x.text)
print("Expected: error")


# curl -X POST http://127.0.0.1:5000/auth -H 'Content-Type: application/json' -H "Authorization: OAuth <ACCESS_TOKEN>" -d '{"username":"cisco","password":"cisco"}'
