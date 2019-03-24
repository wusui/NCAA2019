#!/usr/bin/python
# pylint: disable=W0223
"""
Get a list of teams
"""
from html.parser import HTMLParser
import requests


class ChkTeams(HTMLParser):
    """
    Extract team names from page
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.retval = []

    def handle_starttag(self, tag, attrs):
        for apt in attrs:
            if apt[0] == 'title':
                if apt[1] != "ESPN Search":
                    self.retval.append(apt[1])


DATALOC = "http://www.espn.com/mens-college-basketball/tournament/bracket"


def check_teams():
    """
    Extract a list of teams (schools)
    """
    req = requests.get(DATALOC)
    parser = ChkTeams()
    parser.feed(req.text)
    retv = parser.retval
    return retv[8:]


def make_team_list():
    """
    Call check_teams and stick result in text file
    """
    listv = check_teams()
    with open('teams.txt', 'w') as ofile:
        for team in listv:
            ofile.write(team + '\n')


if __name__ == '__main__':
    make_team_list()
