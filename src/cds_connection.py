"""
 @file cds_connection.py
 
 @author Leonel Caraccioli <leonel@backupnet.com.ar>
 @date 22 august 2019
 @brief AS Device Management
 
 Python3 connector class file for Connection Management on Content Delivery Server of S4C services.
 
 @see 
 
"""

import requests

"""
@brief AS Device Management

Python3 connector class for management devices on Access Server in S4C services.
"""
class cds_connection ():

    connection_id    = None
    connection_token = None
    s4c_last_error   = None
    cds_address      = None
    
    self.session = None
    
    connection_status = s4c_connectionStatus
    
    """
    @brief 

    """
    def __init__(self, connection_id = None, token = None, cds_address = None):
        self.connection_status = s4c_connectionStatus.IDLE
        if connection_id is not None and token is not None and cds_address is not None:
            self.Connect(connection_id, token, cds_address)


    """
    @brief Make POST requests
    
    Make POST request to CDS.
    
    @params url        CDS API Endpoint name.
    @params params     Dictionary params to CDS API funtion invoqued.
    @params FileDown   File object to storage request content, leave None to ignore file storage.
    """
    def request_post(self, url, params, FileDown = None, FileUpl = None):
        
        URL = "http://" + self.cds_address + "/" + url + ".php"
        
        r = self.session.post(url = url, params = params, files = FileUpl)
        
        request_header_content_type = r.header.get('content_type')
        
        if r.status_code == 200:
            if request_header_content_type == 'application/json':
                data = r.json()
                return data
            elif FileDown is not None:
                FileDown.write(r.content)
                return r.header.get('content_type')
            else:
                return None
        else:
            return None
        
    def Connect(self, connection_id = None, token = None, cds_address = None):
        if connection_id is not None: self.connection_id = connection_id
        if token         is not None: self.token         = token
        if cds_address   is not None: self.cds_address   = cds_address
        
        if self.connection_id is not None and self.token is not None and self.cds_address is not None:
            
            self.s4c_last_error = None
            
            self.session = requests.session()
            
            PARAMS = {}
            
            PARAMS["con_id"] = self.connection_id
            PARAMS["token"]  = self.token
            
            data = self.request_post(end_point = "CON_INI", params = PARAMS)
            
            if "exceptionKey" in data:
                self.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return data["data"]
        else:
            return None

    def Status(self):
        if self.as_account is not None and dev_id is not None and dev_id is not "":
            self.s4c_last_error = None
            
            PARAMS = {}
            
            data = self.request_post(end_point = "CON_STA", params = PARAMS)
            
            if "exceptionKey" in data:
                self.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return data["data"]
            
'''         * ClientIP: Your IP as the CDS see it.
            * Counter: Session interactions counter.
            * connection_id: This connection ID.
            * device_id: Connection device own.
            * group_id: Connection device own permission group ID.
            * lastActivity: Connection last Activity.
            * timeout: Connection inactivity timeout in seconds.
            * expiration: Connection expiration.
            * createdTime: Session connection established time.
'''
        else:
            return None

    def Close(self, dev_id):
        if self.as_account is not None and dev_id is not None and dev_id is not "":
            self.s4c_last_error = None
            
            PARAMS = {}
            
            data = self.request_post(end_point = "CON_CLS", params = PARAMS)
            
            if "exceptionKey" in data:
                self.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                if data["data"] == "Sucess":
                    return True
                else:
                    return False
        else:
            return None
    
if __name__ == '__main__':
    
    # Connecting and instantiation
    
    connection = cds_connection(24, "jkh23jk22kj2j2kk23j4jbvk2g3ccf23u", "cds1.backupnet.com.ar")
    
    if connection is not None:
        print("------------  Connected successfully  --------------")
        print("      Connection ID: " + connection.connection_id)
        print("        CDS Address: " + connection.cds_address)
    else:
        print("----------------  No connected  --------------------")
    
    # Getting status
    print()
    print("--------------------  Status  ----------------------")
    
    status = connection.Status()
    
    print("              My IP: " + status["ClientIP"])
    print("   Activity counter: " + status["Counter"])
    print("      Connection ID: " + status["connection_id"])
    print("          Device ID: " + status["device_id"])
    print("           Group ID: " + status["group_id"])
    print("      Last Activity: " + status["lastActivity"])
    print(" Connection Timeout: " + status["timeout"])
    print("         Expiration: " + status["expiration"])
    print(" Connection Created: " + status["createdTime"])
    
    # Clossing connection
    print()
    print("------------------  Clossing  ----------------------")
    
    close = connection.Close()
    
    if close:
        print(" --> Session closed.")
    else:
        print(" --> Clossing error.")
