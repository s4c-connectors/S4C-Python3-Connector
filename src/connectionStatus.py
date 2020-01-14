"""
 @file connectionStatus.py
 
 @author Leonel Caraccioli <leonel@backupnet.com.ar>
 @date 21 august 2019
 @brief Connection status clasess
 
 Python3 connection status.
 
 @see http://s4c.backupnet.com.ar/sdk/python3
 
"""

from enum import Enum, auto

"""

@brief Connection Status

Python3 connection status class.

"""

class s4c_connectionStatus (Enum):
    IDLE = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    FAIL = auto()
    
class s4c_as_connectionData ():
    ClientIP      = ''
    Counter       = 0
    LastTimestamp = ''
    initTime      = ''
    ID_LOG        = 0
    
