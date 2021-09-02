import json
import subprocess as sp

ROOT = './data/'

def workspaces():
    """ Find names of Slack workspaces in data """
    return [
        s for s in sp.run(['ls', ROOT], capture_output = True).stdout.decode('UTF-8').split('\n') if s
    ]

def channels(workspace):
    """ Find names of channels in Slack `workspace` """
    return [
        s[:-5] for s in sp.run(['ls', '{}{}/channels/'.format(ROOT, workspace)], capture_output = True).stdout.decode('UTF-8').split('\n') if s
    ]

def channel_info(workspace, channel):
    """ Get relevant channel info from `channel` in `workspace` """
    path = '{}{}/channels/{}.json'.format(ROOT, workspace, channel)
    with open(path, 'r') as jsonf:
        return json.load(jsonf)['channel_info']

