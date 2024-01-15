from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search

'''
The user need to define the aggregate properties for the breakdown element. 

1. POST /api/bkd/aggr_json/{repository}/{model}/{node}/{prop}/{token}  upload data in JSON format
2. POST /api/bkd/aggr_csv/{repository}/{model}/{node}/{prop}/{token} in upload data in CSV format 

The example for a JList of JSON format data for uploading is shown below and the aggregate properties are created for the element 
in PLM to store accelerometer sensor values and it contains timestamp, acceleration in x,y,z directions

[{"Timestamp": "2023-04-18 09:30:03", "X": 14, "Y": -2, "Z": 9}, {"Timestamp": "2023-04-18 09:30:04", "X": -4, "Y": -5, "Z": -3}, {"Timestamp": "2023-04-18 09:30:05", "X": 12, "Y": 0, "Z": -2}, {"Timestamp": "2023-04-18 09:30:06", "X": 13, "Y": 0, "Z": 9}, {"Timestamp": "2023-04-18 09:30:07", "X": 0, "Y": -9, "Z": 5}]

The example for uploading data in a CSV format data is shown below 

Timestamp,X,Y,Z
2023-04-10 15:30:18,-2,-7,7
2023-04-10 15:30:19,8,7,-7

'''

# Generating random data for uploading 
def generating_sample_data(no_of_records):
    data_accl = []
    for _ in range(no_of_records):
        time.sleep(1)
        currentTimeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        currentx = random.randrange(-5, 15)
        currenty = random.randrange(-10, 10)
        currentz = random.randrange(-10, 10)

        data_accl.append({"Timestamp": currentTimeStamp, "X": currentx, "Y": currenty, "Z": currentz})

    # Writing data to JSON file
    with open("accl_new_file.json", "w") as file:
        json.dump(data_accl, file)
    print("\tData written to accl_new_file.json")

    # Writing data to CSV file
    df_csv = pd.DataFrame(data_accl)
    df_csv.to_csv("accl_new_file.csv", index=False)
    print("\tData written to accl_new_file.csv")
    return 

def upload_data(file_path, url_type, model, node, prop,token,repository = "TruePLMprojectsRep"):
  
    if url_type == 'JSON':
        url_format = "/api/bkd/aggr/{}/{}/{}/{}/{}".format(repository, model, node, prop, token)
    elif url_type == 'CSV':
        url_format = "/api/bkd/aggr_csv/{}/{}/{}/{}/{}".format(repository, model, node, prop, token)
    else:
        print('Invalid URL type')
        return

    url = PLM_URL + url_format

    print("\nPerforming request: " + url)
    try:
        with open(file_path, "r") as file:
            response = requests.post(url, files={"file": file}, timeout=2.0)
            response.raise_for_status()
            return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
    return None   


# Input parameters 

no_of_records=1                                     # required no of records to upload 

generating_sample_data(no_of_records)

file_path = "accl_new_file.json"
url_type = "JSON"                                    # Change this to "CSV" if needed
model = "Palfinger_Crane_Assembly" 
prop = "urn:rdl:" + model + ":Acceleration_reading"  # porperty
search_params={ "case_sens":"false",         
                "domains":"ID",         
                "folder_only":"true",  
                "node":"",              
                "page":"",              
                "page_size":"",        
                "pattern":"Accelerometer_Sensor",   # Required Breakdown element name 
                "props":""}        

token = get_token(getTokenData)
if token: 
    node=str(bd_quick_search(model,'q_search',search_params,token)[0]['bkdn_elem_info']['instance_id']) # Required node number
    print('The required breakdown element Instance Id:',node)
    if node:
        upload_result=upload_data(file_path, url_type, model, node, prop,token)
        if upload_result:
            print('Data uploaded to the Instance {}'.format(node))  
