
from generating_token import get_token,plm_info,headers
import requests



#####################  Retriving sensor data  ###################### 

def get_aggr_data(model, node, prop, data_params, token, repository="TruePLMprojectsRep"):
    endpoint = f"/api/bkd/aggr/{repository}/{model}/{node}/{prop}/{token}"
    get_filtered_data_url = plm_info['url'] + endpoint
    print("\nRequesting data from:", get_filtered_data_url)

    try:
        response = requests.get(get_filtered_data_url,headers=headers, params=data_params, timeout=30.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e.response.status_code} - {e.response.text}')
    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print(f'General Request failed: {e}')
    return None
    

def main():
    model = "Palfinger_Crane_Assembly"
    prop = f"urn:rdl:{model}:acceleration_readings"  
    node = "201863468815"
    data_params = {
        'from': "",        # UNIX timestamp with milliseconds
        'to': "",
        'page':"1",         
        'size':"1",
        'reverse_order':"true"
    }

    token = get_token()
    if token:
        response = get_aggr_data(model, node, prop, data_params, token)
        if response:
            print("Data downloaded:", response)
    else:
        print("Failed to retrieve token.")

if __name__ == "__main__":
    main()
    
    
