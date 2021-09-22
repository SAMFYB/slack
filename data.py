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

def messages(workspace, channel):
    """ Get messages of `channel` in `workspace` """
    path = '{}{}/channels/{}.json'.format(ROOT, workspace, channel)
    with open(path, 'r') as jsonf:
        return json.load(jsonf)['messages']



if '__main__' == __name__:
    import sys
    from pprint import pprint

    if len(sys.argv) > 1:

        if sys.argv[1] == 'workspaces':
            pprint(workspaces())
            sys.exit(0)

        elif sys.argv[1] == 'channels':
            if len(sys.argv) < 3:
                print('Which workspace?')
                sys.exit(1)
            try:
                pprint(channels(sys.argv[2]))
                sys.exit(0)
            except Exception:
                print('Is {} a correct workspace?'.format(sys.argv[2]))
                sys.exit(1)

        elif sys.argv[1] == 'channel-info':
            if len(sys.argv) < 4:
                print('Which workspace and which channel?')
                sys.exit(1)
            try:
                pprint(channel_info(sys.argv[2], sys.argv[3]))
                sys.exit(0)
            except Exception:
                print('Is {} -> {} a correct workspace channel?'.format(sys.argv[2], sys.argv[3]))
                sys.exit(1)

    else:
        print('Options:')
        print('workspaces - Find names of Slack workspaces in data')
        print('channels <workspace> - Find names of channels in Slack `workspace`')
        print('channel-info <workspace> <channel> - Get relevant channel info from `channel` in `workspace`')
        sys.exit(0)

