from generating_token import get_token,plm_info
import requests

'''
The user need to define the aggregate properties for the breakdown element. 

1. POST /api/bkd/aggr_json/{repository}/{model}/{node}/{prop}/{token}  upload data in JSON format
2. POST /api/bkd/aggr_csv/{repository}/{model}/{node}/{prop}/{token} in upload data in CSV format 

The example for a JList of JSON format data for uploading is shown below and the aggregate properties are created for the element 
in PLM to store accelerometer sensor values and it contains timestamp, acceleration in x,y,z directions

[{"Timestamp": "2023-04-18 09:30:03", "X": 14, "Y": -2, "Z": 9},
 {"Timestamp": "2023-04-18 09:30:04", "X": -4, "Y": -5, "Z": -3},
 {"Timestamp": "2023-04-18 09:30:05", "X": 12, "Y": 0, "Z": -2}, 
 {"Timestamp": "2023-04-18 09:30:06", "X": 13, "Y": 0, "Z": 9}, 
 {"Timestamp": "2023-04-18 09:30:07", "X": 0, "Y": -9, "Z": 5}]

The example for uploading data in a CSV format data is shown below 

Timestamp,X,Y,Z
2023-04-10 15:30:18,-2,-7,7
2023-04-10 15:30:19,8,7,-7

'''

def upload_data(file_path, data_format, model, node, prop, token, repository="TruePLMprojectsRep"):
    base_url = plm_info['url']
    if data_format == 'JSON':
        endpoint = f"/api/bkd/aggr/{repository}/{model}/{node}/{prop}/{token}"
    elif data_format == 'CSV':
        endpoint = f"/api/bkd/aggr_csv/{repository}/{model}/{node}/{prop}/{token}"
    else:
        print('Invalid data format specified')
        return

    full_url = base_url + endpoint
    print(f"\nPerforming request: {full_url}")

    try:
        with open(file_path, "rb") as file:  
            response = requests.post(full_url, files={"file": file}, timeout=30.0)
            response.raise_for_status()
            return response.json() if response.ok else None
    except requests.exceptions.Timeout:
        return "Request timed out"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def main():
    file_path = r'files/Accleration_readings_data.json'
    data_format = "JSON"  
    model = "Palfinger_Crane_Assembly"
    prop = f"urn:rdl:{model}:acceleration_readings"  
    node = "201863476589"
    token = get_token()

    if token:
        upload_result = upload_data(file_path, data_format, model, node, prop, token)
        print(upload_result)

if __name__ == "__main__":
    main()