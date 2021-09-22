import data, people

class activity:
    """ Activity in `workspace` APIs """

    def __init__(self, workspace):
        self.workspace = workspace
        self.channels = data.channels(workspace)
        self.messages = dict((channel, data.messages(workspace, channel)) for channel in self.channels)

    def channel_breakdown(self, channel):
        """ Percentage of `channel` activity by users in terms of number of messages """
        members = data.channel_info(self.workspace, channel)
        from collections import Counter
        counter = Counter(message['user'] for message in self.messages[channel])
        s = len(self.messages[channel])
        return [(user, round(count / s * 100)) for user, count in counter.items()]

    def user_breakdown(self, user):
        """ Percentage of `user` activity by channels in terms of number of messages """
        channels = people.get_user_channels(self.workspace, user)
        counter = {}
        for channel in channels:
            counter[channel] = len(list(filter(lambda message: message['user'] == user, self.messages[channel])))
        s = sum(counter.values())
        return [(channel, round(count / s * 100)) for channel, count in counter.items()]

    def user_messages_text(self, user):
        """ Get messages text from `user` grouped by channel """
        channels = people.get_user_channels(self.workspace, user)
        return dict((
            channel,
            [
                message['text'] for message in self.messages[channel] if message['user'] == user
            ]) for channel in channels)

