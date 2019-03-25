#!/usr/bin/python
"""
Read real_world.txt to get either active teams or
game results
"""


def get_survivors():
    """
    Get list of active teams from real_world.txt
    """
    with open('real_world.txt', 'r') as rfile:
        team_data = rfile.readlines()
    retv = []
    for entry in team_data:
        if entry == '\n':
            retv = []
        else:
            retv.append(entry.strip())
    return retv


def get_results():
    """
    Update team win information from real_world.txt
    """
    with open('real_world.txt', 'r') as rfile:
        team_data = rfile.readlines()
    level = 0
    rounds = []
    cround = []
    for team in team_data:
        if team == '\n':
            level += 1
            rounds.append(cround)
            cround = []
        else:
            cround.append(team.strip())
    rounds.append(cround)
    retval = {}
    for entry in rounds[0]:
        retval[entry] = {'wins': 0, 'alive': True}
    for scoreind in range(1, len(rounds)):
        prev = scoreind - 1
        pairings = []
        for match in range(0, len(rounds[prev]), 2):
            pairings.append([rounds[prev][match], rounds[prev][match+1]])
        for winner in rounds[scoreind]:
            retval[winner]['wins'] += 1
            for entry in pairings:
                if winner in entry:
                    loser = entry[0]
                    if loser == winner:
                        loser = entry[1]
                    retval[loser]['alive'] = False
                    break
    return retval


if __name__ == "__main__":
    print(get_results())
