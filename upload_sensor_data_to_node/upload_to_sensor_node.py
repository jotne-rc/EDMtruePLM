import requests
import yaml
import json 
from urllib.parse import quote

# Loading relevant variables to global scope like for now
with open(f'trueplm_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    token_url = config['server'] + config['token_url']

# Can be reused to some extent, but they will expire.
def get_token():
    try:
        response = requests.post(token_url , data=config['credentials'], timeout=2.0)

        if 'token' in response.json():
            return response.json()['token']
        else:
            print("Error: Token not found in the response.")
        
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))

    return None

# uploads json data to a predefined property of a breakdown element
def put_data(search_params, model, property, token, data):

    node = get_node(search_params, target_model, token)
    property = 'urn:rdl:%s:%s' % (model, property)
    upload_url = config['server'] +  config['append_url'] + '/'.join([config['repository'], model, node, quote(property), token])

    try:
        response = requests.post(upload_url, files={"file": data}, timeout=2.0)
        response.raise_for_status()

        if response.ok: 
            return response.json() 
        
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))

    return None   
    
# retrieve node ID from search. *Should* be retrieved, as it can change. 
# simplified to assume one hit for our use case
def search_breakdown(search_params, model, token):
    search_url = config['server'] + '/'.join([config['search_url'], config['repository'], model, token])

    try:
        response = requests.get(search_url, params=search_params, timeout=2.0)
        response.raise_for_status()
        if response.ok:
            return response.json()['result'][0] 
    
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))

    return None

# just a function to call "search breakdown" and retrieve node id from the result.
def get_node(search_params, model, token):
    search_result = search_breakdown(search_params, model, token)

    if search_result:
        return str(search_result['bkdn_elem_info']['instance_id']) 
    else:
        return None

if __name__ == "__main__":
    # declaring these here in case multiple/different models
    target_model = 'project_name' # note that "model" is equivalent to project 
    target_node = "node_name"
    target_property = 'property_name'

    token = get_token()

    if token:
        search_params={
            "domains":      "ID",           # List of subjects for search, can include ID, DESCRIPTION, CLASS, PROPERY
            "folder_only":  "true",         # Return only direct children of parent folder
            "pattern":      target_node,    # Search string pattern (for LIKE operations in EXPRESS)
        }                     

        # just for creating test data
        from datetime import datetime
        ts = datetime.now()

        json_data = '[{"index": "' + str(ts) + '", "val1": 14.7, "val2": -3.2, "val3": 9.6, "val4": 2.1, "val5": 1.0}]'

        # consider calling this async
        put_data(search_params, target_model, target_property, token, json_data) # put main function


 