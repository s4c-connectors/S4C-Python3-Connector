"""
 @file as_connection.py
 
 @author Leonel Caraccioli <leonel@backupnet.com.ar>
 @date 22 august 2019
 @brief AS Connection Management
 
 Python3 connector class file for Connection Management on Access Server of S4C services.
 
 @see 
 
"""

import requests

"""

@brief AS Connection Management

Python3 connector class for management connection on Access Server in S4C services.

"""

class as_connection ():

    s4c_server_address = "http://as.s4c.backupnet.com.ar"

    s4c_last_error = None
    session = None
    
    device_id = None
    device_token = None
    
    connection_id = None
    connection_token = None
    connection_timeout = None
    connection_expiration = None
    connection_status = None
    
    device_name = None
    device_group_id = None
    device_description = None
    device_lastConnection = None
    device_lastActivity = None
    
    cds_address = None
    cds_name = None
    cds_description = None
        
    """
    @brief 

    """
    def __init__(self, device_id = None, token = None):
        if device_id is not None and token is not None:
            self.get(device_id, token)
    
    def request_post(self, end_point, params):
        url = self.s4c_server_address + "/" + end_point
        
        r = self.session.post(url = url, params = params)
        
        request_header_content_type = r.headers['Content-Type']
        
        if r.status_code == 200:
            if request_header_content_type == 'application/json':
                data = r.json()
                return data
            else:
                return None
        else:
            return None
        
    def get(self, device_id = None, token = None):
        self.s4c_last_error = None
        self.session = requests.session()
        
        if device_id is not None: self.device_id = device_id
        if token is not None: self.device_token = token
        
        if self.device_id is None or self.device_token is None:
            self.s4c_last_error = {"process":"get", "error":"device_id and device_token are not optional."}
            return None
        
        PARAMS = {"dev_id":self.device_id, "token":self.device_token}
        
        data = self.request_post(end_point = "AS_CON", params = PARAMS)
        print(data)
        if "exceptionKey" in data:
            self.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
            return None
        elif "data" in data:
            self.connection_id           = data["data"]["con_id"]
            self.connection_token        = data["data"]["token"]
            self.connection_timeout      = data["data"]["connectionTimeout"]
            self.connection_expiration   = data["data"]["connectionExpiration"]
            self.connection_status       = data["data"]["status"]
            
            self.device_name             = data["data"]["name"]
            self.device_description      = data["data"]["description"]
            self.device_group_id         = data["data"]["group_id"]
            self.device_lastConnection   = data["data"]["lastConnection"]
            self.device_lastActivity     = data["data"]["lastActivity"]
            
            self.cds_address             = data["data"]["cds_address"]
            self.cds_name                = data["data"]["cds_name"]
            self.cds_description         = data["data"]["cds_description"]
            
            return self
        else:
            return None

    def status(self):
        if self.connection_id is None or self.device_token is None:
            self.s4c_last_error = {"process":"get", "error":"connection_id and connection_token are not optional."}
            return None
        else:
            self.s4c_last_error = None

            PARAMS = {"con_id":self.connection_id, "token":self.device_token}

            data = self.request_post(end_point = "AS_STA", params = PARAMS)

            if "exceptionKey" in data:
                self.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                self.connection_id           = data["data"]["con_id"]
                self.connection_timeout      = data["data"]["connectionTimeout"]
                self.connection_expiration   = data["data"]["connectionExpiration"]
                self.connection_status       = data["data"]["status"]
                
                self.device_name             = data["data"]["name"]
                self.device_description      = data["data"]["description"]
                self.device_group_id         = data["data"]["group_id"]
                self.device_lastConnection   = data["data"]["lastConnection"]
                self.device_lastActivity     = data["data"]["lastActivity"]
                
                self.cds_address             = data["data"]["cds_address"]
                self.cds_name                = data["data"]["cds_name"]
                self.cds_description         = data["data"]["cds_description"]
                return True
            else:
                return None

    def close(self):
        if self.device_id is None or self.device_token is None:
            self.s4c_last_error = {"process":"get", "error":"device_id and token are not optional."}
            return None
        else:
            self.s4c_last_error = None
            
            PARAMS = {"con_id":self.connection_id, "token":self.device_token}
            
            data = self.request_post(end_point = "AS_CLS", params = PARAMS)
            
            if "exceptionKey" in data:
                self.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return True
            else:
                return None
    
if __name__ == '__main__':
    
    # Connecting and instantiation
    
    connection = as_connection(7, "87f99e32fe0b1b42f0e648a3172c6e42ff66fe895f75eeae533f9ce45ca25d91")
    
    if connection is not None:
        if connection.device_lastConnection is None: connection.device_lastConnection = "Never"
        print("---------  Connection successful created  ----------")
        print(" Connection:")
        print("                   ID: " + str(connection.connection_id))
        print("                Token: " + connection.connection_token)
        print("              Timeout: " + connection.connection_timeout)
        print("           Expiration: " + connection.connection_expiration)
        print("               Status: " + (connection.connection_status if connection.connection_status is not None else ""))
        print(" Device:")
        print("                   ID: " + str(connection.device_id))
        print("                Token: " + connection.device_token)
        print("                 Name: " + (connection.device_name if connection.device_name is not None else ""))
        print("          Description: " + (connection.device_description if connection.device_description is not None else ""))
        print("             Group ID: " + connection.device_group_id)
        print("      Last Connection: " + connection.device_lastConnection)
        print("        Last Activity: " + (connection.device_lastActivity if connection.device_lastActivity is not None else ""))
        print(" CDS:")
        print("              Address: " + connection.cds_address)
        print("                 Name: " + connection.cds_name)
        print("          Description: " + connection.cds_description)
    else:
        print("No connected")
    
    status = connection.status()
    
    if status:
        print("-----------  Connection status updated  ------------")
        print(" Connection:")
        print("                   ID: " + str(connection.connection_id))
        print("                Token: " + connection.connection_token)
        print("              Timeout: " + connection.connection_timeout)
        print("           Expiration: " + connection.connection_expiration)
        print("               Status: " + (connection.connection_status if connection.connection_status is not None else ""))
        print(" Device:")
        print("                   ID: " + str(connection.device_id))
        print("                Token: " + connection.device_token)
        print("                 Name: " + (connection.device_name if connection.device_name is not None else ""))
        print("          Description: " + (connection.device_description if connection.device_description is not None else ""))
        print("             Group ID: " + connection.device_group_id)
        print("      Last Connection: " + connection.device_lastConnection)
        print("        Last Activity: " + (connection.device_lastActivity if connection.device_lastActivity is not None else ""))
        print(" CDS:")
        print("              Address: " + connection.cds_address)
        print("                 Name: " + connection.cds_name)
        print("          Description: " + connection.cds_description)
    else:
        print("No connected")
    
    close = connection.close()
    
    if close:

        status = connection.status()
        
        if status:
            print("-----------  Connection status updated  ------------")
            print(" Connection:")
            print("                   ID: " + str(connection.connection_id))
            print("              Timeout: " + connection.connection_timeout)
            print("           Expiration: " + connection.connection_expiration)
            print("               Status: " + (connection.connection_status if connection.connection_status is not None else ""))
        else:
            print("No connected")
        
