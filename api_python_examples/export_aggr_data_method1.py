from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search

'''
To download aggregate data the following API calls are required:

1./api/bkd/aggr_exp/{repository}/{model}/{node}/{prop}/{token}, Export the values of the aggregated property with paging and filtering to the JSON format

2. /api/dat/file/data/{src}/{name}/{token}, Return file data for download

The first method takes inputs parameters to get data in required format either CSV or JSON . This method will generate 
file properties as shown in below example.

    {'descr': None,
    'source': 'aggr6673349257703198929down',
    'contentType': None, 
    'discipline': None, 
    'projPhase': None, 
    'status': None, 
    'editor': None, 
    'resp': None, 
    'rev': None, 
    'app': None, 
    'revMan': None, 
    'title': 'Accleration_readings_data.csv',
    'isNewIssue': False}

The source and title values are supplied to the second API function from this response.

The example for output response in csv format is shown below 

Timestamp,X,Y,Z

2023-04-11 06:31:04,0,-6,-9
2023-04-11 06:31:05,12,-4,8
2023-04-11 06:31:06,9,7,-9

The example for output resposne in JSON  format is shown below 

[{"Timestamp":"2023-04-11 06:31:04","X":"0","Y":"-6","Z":"-9"},
{"Timestamp":"2023-04-11 06:31:05","X":"12","Y":"-4","Z":"8"},
{"Timestamp":"2023-04-11 06:31:06","X":"9","Y":"7","Z":"-9"}]


'''

def get_data_prop(model,node,prop,data_params,token,repository="TruePLMprojectsRep"):
    
    download_data_file_prop = PLM_URL + "/api/bkd/aggr_exp/" + repository + "/" + model + "/" + node + "/" + prop + "/" + token

    print("\nPerforming request:", download_data_file_prop)
    try:
        response = requests.get( download_data_file_prop,params=data_params, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None   
        
def aggr_download_data(file_prop,token):  
    
    if file_prop:
        print('The rerquired file properties',file_prop)
        download_data_url = PLM_URL+"/api/dat/file/data/"+file_prop['source']+"/"+file_prop['title']+"/"+token

        print("\nPerforming request:",download_data_url)

        try:
            response = requests.get(download_data_url, timeout=2.0)
            response.raise_for_status()
            return response.json() if response.ok else None
        except requests.exceptions.RequestException as e:
            print('Request failed {}\nError Message:  {}'.format(e, response.text))
            return None  
    else:  
        print('Not valid file properties')
        
    
model="Palfinger_Crane_Assembly"                      # porject name

prop = "urn:rdl:" + model + ":Acceleration_reading"  # porperty

data_params={'from':"",               # date format for should be unix format with milliseconds(example:1686029024000)
            'to':"",
            'format':'json',          # csv or json
            'cols':[]}                # Example to select required cols ['x','z']
    
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
        data = get_data_prop(model, node, prop, data_params, token)
        if data:
            data_response = aggr_download_data(data, token)
            if data_response:
                print(data_response)