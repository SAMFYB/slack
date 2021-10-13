import data, people

class activity:
    """ Activity in `workspace` APIs """

    def __init__(self, workspace):
        self.workspace = workspace
        self.channels = data.channels(workspace)
        self.messages = dict((channel, data.messages(workspace, channel)) for channel in self.channels)

    def channels_breakdown(self, percentage_over = 0, total_messages_over = 0, include_single_member_channels = True):
        """ Percentage of channel activity by users for channels satisfying given filters in this workspace """
        has_percentage_over = lambda breakdown: any(percentage > percentage_over for _, _, percentage, _ in breakdown)
        total_messages_is_over = lambda breakdown: sum(count for _, _, _, count in breakdown) > total_messages_over
        is_single_member_channel = lambda breakdown: len(breakdown) <= 1
        breakdowns = [(channel, self.channel_breakdown(channel)) for channel in self.channels]
        filtered = [
            (channel, breakdown) for channel, breakdown in breakdowns \
            if has_percentage_over(breakdown) and \
               total_messages_is_over(breakdown) and \
               (include_single_member_channels or not is_single_member_channel(breakdown))
        ]
        print(f'{len(breakdowns) = }, {len(filtered) = }')
        return dict(filtered)

    def channel_breakdown(self, channel):
        """ Percentage of `channel` activity by users in terms of number of messages """
        members = data.channel_info(self.workspace, channel)
        from collections import Counter
        counter = Counter(message['user'] if 'user' in message else 'N/A' for message in self.messages[channel])
        s = len(self.messages[channel])
        return [( # user ID, role (reference), percentage, count (# messages)
            user,
            people.reference_users[user]['role'] if user in people.reference_users else None,
            round(count / s * 100),
            count
            ) for user, count in counter.items()]

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

    def channel_timeline(self, channel):
        """ Get timeline of activity (messages) in `channel` """
        timeline = [float(message['ts']) for message in self.messages[channel]]
        breaks = [(timeline[i] - timeline[i + 1], (timeline[i + 1], timeline[i])) for i in range(len(timeline) - 1)]
        from statistics import median
        median_break = round(median([brk for brk, _ in breaks]))
        def Hampel(L, m):
            """ Identify indices for Hampel outliers given data `L` and median `m` """
            # ref https://towardsdatascience.com/practical-implementation-of-outlier-detection-in-python-90680453b3ce
            deviations = [abs(x - m) for x in L]
            median_deviation = median(deviations)
            return [i for i in range(len(L)) if abs(L[i] - m) >= 4.5 * median_deviation]
        return {
            'timeline': timeline,
            'median_break': median_break, # "Activity level", ref (Mezouar) `Exploring the Use of Chatrooms`
            'outliers': [breaks[i] for i in Hampel([brk for brk, _ in breaks], median_break)],
        }



if '__main__' == __name__:
    import sys
    from pprint import pprint

    opts = dict([
        (key, value) for key, value in [
            opt.split(':') for opt in sys.argv[1:]
        ]
    ])

    if 'channels-breakdown' in opts:
        workspace = opts['channels-breakdown']
        pprint(activity(workspace).channels_breakdown(
            percentage_over = int(opts['percentage-over']) if 'percentage-over' in opts else 0,
            total_messages_over = int(opts['total-messages-over']) if 'total-messages-over' in opts else 0,
            include_single_member_channels = opts['include-single-member-channels'] == 'yes' if 'include-single-member-channels' in opts else True,
        ))

