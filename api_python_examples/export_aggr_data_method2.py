from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search

'''
To download aggregate data the following API is required. which returns the records in a array of values.

GET /api/bkd/aggr/{repository}/{model}/{node}/{prop}/{token} Return the values of the aggregated property 
with paging and filtering.

This method returns the records in reverse order if-required. 

'''
#####################  downloading sensor data  ###################### 

def get_data_aggr(model,node,prop,data_params,token,repository="TruePLMprojectsRep"):
    
    download_aggr_data = PLM_URL + "/api/bkd/aggr/" + repository + "/" + model + "/" + node +\
    "/" + prop + "/" + token

    print("\nPerforming request:", download_aggr_data)
    try:
        response = requests.get(download_aggr_data,params=data_params, timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None  

#################### parameters required #############
    
model="Palfinger_Crane_Assembly"                      # porject name
prop = "urn:rdl:" + model + ":Acceleration_reading"  # porperty

data_params={'from':"",             # date format should be unix with milliseconds(example:1686029024000)
            'to':"",                # date format should be unix with milliseconds(example:1686029024000)
            'format':'',            # csv or json
            'page':'',              
            'size':'',
            'reverse_order':''}     # Use reverse order of the records           
    
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
        data=get_data_aggr(model,node,prop,data_params,token) 
        if data:
            print(data)  
    