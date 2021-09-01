import json

def get_obj(destination):
    with open(destination, 'r') as f:
        return json.load(f)

def members(destination):
    return get_obj(destination)['channel_info']['members']
