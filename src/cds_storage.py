"""
 @file cds_storage.py
 
 @author Leonel Caraccioli <leonel@backupnet.com.ar>
 @date 22 august 2019
 @brief AS Device Management
 
 Python3 connector class file for File Storage Operations on Content Delivery Server of S4C services.
 
 @see 
 
"""

from cds_connection import cds_connection
import requests

class ReturnFileProperties(object):
  __slots__ = ["size", "path"]
  def __init__(self, size, path):
     self.size = size
     self.path = path

"""
@brief AS Device Management

Python3 connector class for management devices on Access Server in S4C services.
"""
class cds_storage ():

    cds_con = None
    s4c_last_error = None
    
    """
    @brief 

    """
    def __init__(self, cds_con_obj = None, connection_id = None, token = None, cds_address = None):
        if cds_con_obj is not None:
            self.cds_con = cds_con_obj
        elif connection_id is not None and token is not None and cds_address is not None:
            self.cds_con = cds_connection(connection_id, token, cds_address)

    def Upload(self, file_name = None, comment = None):
        if self.cds_con is not None:
            self.cds_con.s4c_last_error = None
            
            PARAMS = {}
            
            if name is not None:        PARAMS["name"]        = name
            if description is not None: PARAMS["description"] = description
            if group_id is not None:    PARAMS["group_id"]    = group_id
            
            data = self.cds_con.request_post(end_point = "FILE_STR", params = PARAMS)
            
            if "exceptionKey" in data:
                self.cds_con.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return data["data"]
        else:
            return None


    """
    @brief Download a file from CDS
    
    Get a file from CDS.
    
    @param file_id          File ID in server.
    @param file_name        Destination file name. 
                            If you leave it blank or None, will take a temporary file name.
                            If you leave a directory the file will be storage inside it with a unique filename.
                            If you set a full filename the file will be stored there.
    @param file_orig_name   If file_name is blank, None or a directory this parameter will set if the name is the original (True) or a temporary filename (Flase, default value). @todo: not working
    
    @return None if an error happended or file data list:
    """
    def Download(self, file_id = None, file_name = None, file_orig_name = False):
        if self.cds_con is not None and dev_id is not None and dev_id is not "":
            self.cds_con.s4c_last_error = None
            
            PARAMS = {"file_id":file_id}
            
            temp_file = None
            
            if file_name is None or os.path.isdir(file_name):
                if os.path.isdir(file_name):
                    tempfile.tempdir = file_name
                file_dwn = tempfile.NamerdTemporaryFile(prefix="cds_", suffix="_downloaded", mode='w+t')
            else:
                file_dwn = open(file_name, 'wb')
            
            data = self.cds_con.request_post(end_point = "FILE_DWN", params = PARAMS, File = file_dwn)
            
            file_dwn.close()
            
            if "exceptionKey" in data:
                self.cds_con.s4c_last_error = {"process":"download", "error":data["exceptionKey"]}
                return None
            elif data is not None:
                returnValue = ReturnFileProperties(size = os.stat.st_size, path = file_dwn.name)
                return returnValue
            else:
                return None

    def List(self):
        if self.cds_con is not None and dev_id is not None and dev_id is not "":
            self.cds_con.s4c_last_error = None
            
            PARAMS = {}
            
            data = self.cds_con.request_post(end_point = "FILE_LS", params = PARAMS)
            
            if "exceptionKey" in data:
                self.cds_con.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return data["data"]
        else:
            return None

    def Delete(self, file_id):
        if self.cds_con is not None and dev_id is not None and dev_id is not "":
            self.cds_con.s4c_last_error = None
            
            PARAMS = {"file_id":file_id}
            
            data = self.cds_con.request_post(end_point = "FILE_DEL", params = PARAMS)
            
            if "exceptionKey" in data:
                self.cds_con.s4c_last_error = {"process":"connection", "error":data["exceptionKey"]}
                return None
            elif "data" in data:
                return data["data"]
        else:
            return None

if __name__ == '__main__':
    
    # Connecting with an internal connection object.

    storage = cds_storage(connection_id = 24, token = "jkh23jk22kj2j2kk23j4jbvk2g3ccf23u", cds_address = "cds1.backupnet.com.ar")
    
    # Or use a external connection module:
    # connection = cds_connection(24, "jkh23jk22kj2j2kk23j4jbvk2g3ccf23u", "cds1.backupnet.com.ar")
    # storage = cds_storage(cds_con_obj = connection)
    
    # List all files
    
    storage_list = storage.List()
    
    print("-----------------  Files List  ---------------------")
    if storage_list is not None:
        if len(storage_list) > 0:
            for element in storage_list:
                print("File ID: %3d  Parant File: %3d".format(element["id"], element["parent_file"]))
                print("          File Name:  %3s Extension:  %3s Mime Type: %3d".format(element["name"], element["extension"], element["size"]))
                print("          File Size: " + element["size"])
                print("      Creation Time: %4s Modification Time: %5s".format(element["creationTime"], element["modificationTime"]))
                print("            Comment: " + element["comment"])
                print("             Status: " + element["status"])
        else:
            print("File List Empty")
    else:
        print("Error getting file list.")
    
    # Upload File
    print()
    print("-----------------  Upload file  --------------------")

    # Create a Temporary file
    import os
    import tempfile
    tf = tempfile.NamedTemporaryFile()
    with open(tf.name, 'wb') as fout:
        fout.write(os.urandom(15024))
        fout.close()
        
    upload_status = storage.Upload(tf.name, "A testing temporary file.")
    
    if upload_status is not None:
        print("File ID: %3d  File Name:  %3s Extension:  %3s Mime Type: %3d".format(upload_status["file_id"], upload_status["file_name"], upload_status["file_ext"], upload_status["file_type"]))
        print("          File Size: ".format(upload_status["file_size"], upload_status["file_hash"]))
        print("            Comment: " + upload_status["file_comment"])

    os.remove(tf.name)

    # Download File
    print()
    print("----------------  Downoad File  --------------------")
    
    download_status = storage.Download(upload_status["fiel_id"])

    if new_device is not None:
        print("          Device ID: " + str(new_device["dev_id"]))
        print("        Device Name: " + new_device["name"])
        print(" Device Description: " + new_device["description"])
        print("  Permissions Group: " + new_device["group_id"])
        print("    Generated Token: " + new_device["token"])

    # Delete File
    print()
    print("------------------  Delete file  -------------------")
    
    new_token = device.newToken(new_device["dev_id"])

    if new_token is not None:
        print("    Generated Token: " + new_token["token"])

    # Clossing connection
    print()
    print("------------------  Clossing  ----------------------")
    
    if close:
        print(" --> Session closed.")
    else:
        print(" --> Clossing error.")
