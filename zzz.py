import requests, random
from flask import jsonify

exam= 'cds'
gender= 'male'
pref= 'afa'
dob= '2005-10-28'


response = requests.get(f'https://upscapi.pythonanywhere.com/play?exam={exam}&gender={gender}&pref={pref}&dob={dob}')


if response.status_code != 204:  
    response1= response.json()
    response2= dict(response1)
    print(list(response2.values())[0])



elif response.status_code==204:
    print("error")

