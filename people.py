import data

def get_user_channels(workspace, user):
    """ Find channels in `workspace` where the `user` is a member """
    channels = data.channels(workspace)
    return [channel for channel in channels if user in data.channel_info(workspace, channel)['members']]

