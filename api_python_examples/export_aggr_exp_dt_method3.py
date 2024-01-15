from generating_token  import *  
from generating_token import get_token
from breakdown_quick_search import bd_quick_search

'''
This method is available from PLM version 3.5.x.x and this gives us the data export options in either CSV or JSON format and reduces the  need for 
using multiple API methods to export data.

/api/bkd/aggr_exp_dt/{repository}/{model}/{node}/{prop}/{token} Export the values of the aggregated property with paging and filtering to the JSON format
'''


#####################  downloading sensor data  ###################### 
def download_aggr_data(model,node,prop,data_params,token,repository="TruePLMprojectsRep"):
                     
    get_filtered_data_url =PLM_URL+ "/api/bkd/aggr_exp_dt/" + repository + "/" + model + "/" + node + \
                                                                                          "/" + prop + "/"+token
    print("\nPerforming request:",get_filtered_data_url)

    try:
        response = requests.get(get_filtered_data_url, params=data_params,timeout=2.0)
        response.raise_for_status()
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print('Request failed {}\nError Message:  {}'.format(e, response.text))
        return None  
    
model="Palfinger_Crane_Assembly"                      # project name

prop = "urn:rdl:" + model + ":Acceleration_reading"  # porperty

data_params={'from':"",             # date format should be unix with milliseconds(example:1686029024000)
            'to':"",
            'format':'json',                     # csv or json
            'cols':['X','Z']}                    # cols ['x','z']

    
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
        data=download_aggr_data(model,node,prop,data_params,token) 
        if data:
            print(data)  
    
    