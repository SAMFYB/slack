import csv
import data

def _read_reference_users():
    with open('users.csv', 'r') as f:
        return dict([(user['id'], user) for user in csv.DictReader(f)])
reference_users = _read_reference_users()

def get_user_channels(workspace, user):
    """ Find channels in `workspace` where the `user` is a member """
    channels = data.channels(workspace)
    return [channel for channel in channels if user in data.channel_info(workspace, channel)['members']]

def workspace_users(workspace):
    """ All users in `workspace` and channels where they are member """
    channels = data.channels(workspace)
    users = {}
    for channel in channels:
        members = data.channel_info(workspace, channel)['members']
        for member in members:
            if member not in users:
                users[member] = []
            users[member].append(channel)
    return users

