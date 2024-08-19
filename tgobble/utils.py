import os
import json
import base64
import uuid
import time
import datetime

def generate_timestamp():
    '''
    Generate a timestamp in seconds since the epoch.
    '''
    return time.time()

def generate_datetime_timestamp(timestamp: float):
    '''
    Generate a datetime string from a float timestamp.
    '''
    return datetime.datetime.fromtimestamp(timestamp).isoformat()

def generate_uuid():
    '''
    Generate a UUID.
    '''
    return str(uuid.uuid4())

def to_base64(string: str):
    '''
    Convert a string to base64.
    '''
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')

def from_base64(string: str):
    '''
    Convert a base64 string to a string.
    '''
    return base64.b64decode(string.encode('utf-8')).decode('utf-8')
