"""
 @file as_device.py
 
 @author Leonel Caraccioli <leonel@backupnet.com.ar>
 @date 22 august 2019
 @brief AS Device Management
 
 Python3 connector class file for Device Management on Access Server of S4C services.
 
 @see 
 
"""


from connectionStatus import s4c_connectionStatus
from connectionStatus import s4c_as_connectionData
from as_account import as_account
import requests

"""

@brief AS Device Management

Python3 connector class for management devices on Access Server in S4C services.

"""

class as_device ():

    as_account = None
    s4c_last_error = None
    
    """
    @brief 

    """
    def __init__(self, user_name = None, user_password = None):
        if user_name is not None and user_password is not None:
            self.as_account = as_account(user_name, user_password)
            if self.as_account is not None:
                self.s4c_last_error = self.as_account.s4c_last_error

    def register(self, name = None, description = None, group_id = None):
        if self.as_account is not None:
            self.as_account.s4c_last_error = None
            
            PARAMS = {}
            
            if name is not None:        PARAMS["name"]        = name
            if description is not None: PARAMS["description"] = description
            if group_id is not None:    PARAMS["group_id"]    = group_id
            
            data = self.as_account.request_post(end_point = "AS_DEV_REG", params = PARAMS)
            
            if data is None:
                return None
            elif "exceptionKey" in data:
                self.as_account.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return data["data"]
            else:
                return None
        else:
            return None


    def newToken(self, dev_id):
        if self.as_account is not None and dev_id is not None and dev_id is not "":
            self.as_account.s4c_last_error = None
            
            PARAMS = {"dev_id":dev_id}
            
            data = self.as_account.request_post(end_point = "AS_DEV_TOKEN", params = PARAMS)
            
            if "exceptionKey" in data:
                self.as_account.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return data["data"]
            else:
                return None
        else:
            return None

    def unregister(self, dev_id):
        if self.as_account is not None and dev_id is not None and dev_id is not "":
            self.as_account.s4c_last_error = None
            
            PARAMS = {"dev_id":dev_id}
            
            data = self.as_account.request_post(end_point = "AS_DEV_UREG", params = PARAMS)
            
            if "exceptionKey" in data:
                self.as_account.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
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
    
    device = as_device(user_name = "leonel", user_password = "123456789")
    
    if device is not None:
        print("------------  Connected successfully  --------------")
        print("               User: " + device.as_account.user_name)
        print("           Password: " + device.as_account.user_password)
        print("             Server: " + device.as_account.s4c_server_address)
    else:
        print("No connected")
    
    # Getting status
    print()
    print("--------------------  Status  ----------------------")
    
    status = device.as_account.Connect_Status()

    if status is None:
        print("   No connected.")
    else:
        print("              My IP: " + status.ClientIP)
        print("  Connection number: " + str(status.ID_LOG))
        if status.LastTimestamp is None: status.LastTimestamp = "Never"
        print("    Last connection: " + status.LastTimestamp)

    # Add device
    print()
    print("---------------  Add a new device  -----------------")
    
    new_device = device.register(name = "First", description = "My first device", group_id = 1)

    if new_device is not None:
        print("          Device ID: " + str(new_device["dev_id"]))
        print("        Device Name: " + new_device["name"])
        print(" Device Description: " + new_device["description"])
        print("  Permissions Group: " + new_device["group_id"])
        print("    Generated Token: " + new_device["token"])
        
        # Get new token
        print()
        print("---------------  Get a new token  ------------------")
        
        new_token = device.newToken(new_device["dev_id"])
        
        if new_token is not None:
            print("    Generated Token: " + new_token["token"])
        
        # New device unregister (delete)
        print()
        print("-----------  Unregister the new token  -------------")
        
        # unregistration = device.unregister(new_device["dev_id"])
        
        #if unregistration == True:
        #    print(" --> Device " + str(new_device["dev_id"]) + " unregistered.")
        #else:
        #    print(" --> Device " + str(new_device["dev_id"]) + " unregistration failed.")
    else:
        print("    Device creation fail.")
        
    # Clossing connection
    print()
    print("------------------  Clossing  ----------------------")

    close = device.as_account.Connect_Close()

    if close:
        print(" --> Session closed.")
    else:
        print(" --> Clossing error.")
