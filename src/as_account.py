"""
 @file as_account.py
 
 @author Leonel Caraccioli <leonel@backupnet.com.ar>
 @date 21 august 2019
 @brief AS Account Management
 
 Python3 connector class file for Account Management on Access Server of S4C services.
 
 @see 
 
"""


from connectionStatus import s4c_connectionStatus
from connectionStatus import s4c_as_connectionData
import requests

"""

@brief AS Account Management

Python3 connector class for management the accounts on Access Server in S4C services.

"""

class as_account ():
    
    #https://2.python-requests.org/en/master/  
    
    s4c_server_address = "http://as.s4c.backupnet.com.ar/"
    user_name          = ""
    user_password      = ""
    last_error         = None
    
    s4c_connection_status = s4c_connectionStatus
    s4c_connection_data   = s4c_as_connectionData
    
    session = None
    
    """
    @brief 

    """
    def __init__(self, user_name = None, user_password = None):
        self.s4c_connection_status = s4c_connectionStatus.IDLE
        
        if user_name is not None and user_password is not None:
            self.Connect(user_name, user_password)
    
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
    
    def SetUserName(self, name):
        self.user_name = name
        
    def SetUserPassword(self, password):
        self.user_password = password
        
    def Connect(self, user_name = None, user_password = None):
        if self.s4c_connection_status == s4c_connectionStatus.IDLE or self.s4c_connection_status == s4c_connectionStatus.FAIL:
            self.s4c_last_error = None

            if user_name is not None:     self.user_name     = user_name
            if user_password is not None: self.user_password = user_password
            
            self.session = requests.session()
            self.s4c_connection_status = s4c_connectionStatus.CONNECTING
    
            # defining a params dict for the parameters to be sent to the API 
            PARAMS = {'user':self.user_name, 'pass':self.user_password} 

            data = self.request_post(end_point = "AS_LOG", params = PARAMS)
    
            if "exceptionKey" in data:
                self.s4c_connection_status = s4c_connectionStatus.FAIL
                self.s4c_last_error        = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                if data["data"] == 'loginSucess':
                    self.s4c_connection_status = s4c_connectionStatus.CONNECTED
                    return True
            else:
                return None
        else:
            return None
            
    def Connect_Status(self):
        if self.s4c_connection_status == s4c_connectionStatus.CONNECTED:
            self.s4c_last_error = None
            
            PARAMS = {} 
            data = self.request_post(end_point = "AS_LOG_STA", params = PARAMS)
            
            if "exceptionKey" in data:
                if data["exceptionKey"] == "noLogin":
                    self.s4c_connection_status = s4c_connectionStatus.FAIL
                self.s4c_last_error        = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                self.s4c_connection_data.ClientIP      = data["data"]["ClientIP"]
                self.s4c_connection_data.Counter       = data["data"]["Counter"]
                self.s4c_connection_data.LastTimestamp = data["data"]["LastTimestamp"]
                self.s4c_connection_data.initTime      = data["data"]["initTime"]
                self.s4c_connection_data.ID_LOG        = data["data"]["ID_LOG"]
                
                return self.s4c_connection_data
        else:
            return None
        
    def Connect_Close(self):
        if self.s4c_connection_status == s4c_connectionStatus.CONNECTED:
            self.s4c_last_error = None
            
            PARAMS = {} 
            data = self.request_post(end_point = "AS_LOGOUT", params = PARAMS)
            
            if "exceptionKey" in data:
                if data["exceptionKey"] == "noLogin":
                    self.s4c_connection_status = s4c_connectionStatus.FAIL
                    self.s4c_last_error        = {"process":"connection", "error":data["exceptionKey"]}
                    return False
            elif "data" in data:
                if data["data"] == "loginClosed":
                    self.session = None
                    self.s4c_connection_status = s4c_connectionStatus.IDLE
                    return True
        else:
            return False
        
        
        
if __name__ == '__main__':
    
    # Connecting and instantiation
    
    connection = as_account("leonel", "123456789")
    
    if connection is not None:
        print("------------  Connected successfully  --------------")
        print("               User: " + connection.user_name)
        print("           Password: " + connection.user_password)
        print("             Server: " + connection.s4c_server_address)
    else:
        print("No connected")
    
    # Getting status
    print()
    print("------------------  Status  ------------------------")
    
    status = connection.Connect_Status()
    
    if status is None:
        print("   No connected.")
    else:
        print("              My IP: " + status.ClientIP)
        print("  Connection number: " + str(status.ID_LOG))
        print("    Last connection: " + status.LastTimestamp)
        

    # Clossing connection
    print()
    print("------------------  Clossing  ----------------------")

    close = connection.Connect_Close()

    if close:
        print(" --> Session closed.")
    else:
        print(" --> Clossing error.")
