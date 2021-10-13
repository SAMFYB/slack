import csv
from people import workspace_users, get_user_channels

def _read():
    with open('users.csv', 'r') as f:
        return [row for row in csv.DictReader(f)]

users = _read()

# hackathons and roles identified by reference users.csv
hackathons = set([user['hackathon_id'] for user in users])
roles = set([user['role'] for user in users])
print(f'{hackathons = }')
print(f'{roles = }')

# verify user IDs are unique across reference users.csv
by_user = {} # user ID -> user object
for user in users:
    id = user['id']
    assert id not in by_user
    by_user[id] = user

# validate hackathon users
assert hackathons == {'hackthecrisis', 'hackthecrisisafghanistan', 'hackthecrisisindia', 'TGH'}
tgh_workspace = 'theglobalhack'
def _validate_hackathon(hackathon, workspace):
    reference_hackathon_users = [id for id, user in by_user.items() \
                                if user['hackathon_id'] == hackathon]
    from_dataset = workspace_users(workspace) # user ID -> list of channels
    try:
        assert set(from_dataset.keys()) == set(reference_hackathon_users)
    except AssertionError:
        X = set(from_dataset.keys())
        R = set(reference_hackathon_users)
        print(
            hackathon,
            f'{len(X - R) = }', X - R if len(X - R) <= 10 else '...',
            f'{len(R - X) = }', R - X if len(R - X) <= 10 else '...',
        )
for hackathon in hackathons:
    if hackathon == 'TGH':
        continue
    _validate_hackathon(hackathon, hackathon)

