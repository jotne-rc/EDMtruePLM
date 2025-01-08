import requests
import yaml
import json 
from urllib.parse import quote

# Loading relevant variables to global scope like for now
# see "upload_sensor_data_to_node"
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


def get_baseline_ddi_spreadsheet(token):
    target = f"{config['server']}/{config['ddi_export_url']}/{config["repository"]}/{config["model"]}/TDP_init"

    headers = {
    'Authorization': token
    }

    response = requests.get(target, headers=headers, timeout=20.0, allow_redirects=True)

    filename = response.json()["title"]
    
    target = f"{config['server']}/api/dat/file/data/{response.json()["source"]}/{response.json()["title"]}"

    response = requests.get(target, headers=headers, timeout=20.0, allow_redirects=True, stream=True)
    open(filename, 'wb').write(response.content)


if __name__ == "__main__":
    target_model = 'test_remove_files' # note that "model" is equivalent to project 

    token = get_token()

    # ddi export api call - a file will be created in the running directory 
    get_baseline_ddi_spreadsheet(token)
    
    
