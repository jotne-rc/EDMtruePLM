import requests
import numpy as np
import sys
import time
import random
import datetime
import json
import pprint
import csv
import json
import pandas as pd
from pathlib import Path
pp=pprint.PrettyPrinter()



def get_token(getTokenData):
    try:
        print("Performing request: " + get_token_url )
        response = requests.post(get_token_url , data=getTokenData, timeout=2.0)
        response.raise_for_status()
        if 'token' in response.json():
            token = response.json()["token"]
            return token
        else:
            print("Error: Token not found in the response.")
    except requests.exceptions.RequestException as e:
         print('Request failed {}\nError Message:  {}'.format(e, response.text))
         
         
# Loading config.josn file 

config_file = open('config.json')
plm_info= json.load(config_file)


PLM_URL = plm_info['url']         # change this to project specific URL
get_token_url = PLM_URL + "/api/admin/token"             # API to get token

response={}  

getTokenData = {
    "group": "sdai-group",             # User group,Default parameter for All users
    "user": plm_info['user_name'],    # PLM User name
    "pass": plm_info['password']      # PLM Password
}

token = get_token(getTokenData)
if token:
    print("The token is:", token)

