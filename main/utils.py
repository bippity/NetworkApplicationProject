'''
utils class
Provides useful functions/classes
https://github.com/bippity/NetworkApplicationProject/
'''
import json

class Addresses:
    CONTROLLER = "10.0.0.1"
    SERVER = "10.0.0.2"
    RENDERER = "10.0.0.3"
    
class Ports:
    SERVER = 1234
    RENDERER = 1235
    
class MessageTypes:
    FETCH = 0
    REQUEST = 1
    RESPONSE = 2
    EXIT = 3
    ERROR = 4
    
#Efficiently decode unicode back to its original form from JSON
#https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json    
def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )
        
def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )
    
def _byteify(data, ignore_dicts = False):
    # If this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
        
    # If this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
        
    # If this is a dictionary, return dictionary of byteified keys and values
    #but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # If it's anything else, return its original form
    return data