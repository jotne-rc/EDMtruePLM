
from generating_headers import plm_info, headers
import requests

'''
This method is available from PLM version 3.5.x.x and this gives us the data export options in either CSV or JSON format and reduces the  need for 
using multiple API methods to export data.

/api/bkd/aggr_exp_dt/{repository}/{model}/{node}/{prop} Export the values of the aggregated property with paging and filtering to the JSON format
'''

#####################  downloading sensor data  ###################### 
def download_aggr_data(model, node, prop, data_params, repository="TruePLMprojectsRep"):
    endpoint = f"/api/bkd/aggr_exp_dt/{repository}/{model}/{node}/{prop}"
    get_filtered_data_url = plm_info['url'] + endpoint
    print("\nRequesting data from:", get_filtered_data_url)

    try:
        response = requests.get(get_filtered_data_url, headers=headers, params=data_params, timeout=30.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.Timeout:
        return "Request timed out"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    
def main():
    model = "Palfinger_Crane_Assembly"
    prop = f"urn:rdl:{model}:acceleration_readings"  
    node = "201863476589"
    data_params = {
        'from': "",        # UNIX timestamp with milliseconds
        'to': "",
        'format': 'json',  # csv or json
        'cols': []         # filter cols ['x','z']
    }

    response = download_aggr_data(model, node, prop, data_params)
    if response:
        print("Data downloaded:", response)
    else:
        print(response.text)
  

if __name__ == "__main__":
    main()
    
    