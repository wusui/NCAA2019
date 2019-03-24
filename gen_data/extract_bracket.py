#!/usr/bin/python
# pylint: disable=W0223
from html.parser import HTMLParser
import os
import sys
import codecs
import json
import requests
from get_group import get_group


HEADER = 'http://fantasy.espn.com/tournament-challenge-bracket/'
HEADER += '2019/en/entry?entryID='


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class GetBracket(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.name = ''
        self.picks = {}
        self.name_flag = False
        self.pick_flag = False

    def handle_starttag(self, tag, attrs):
        for apt in attrs:
            if apt[0] == 'class':
                if apt[1] == 'entry-details-entryname':
                    self.name_flag = True
                if apt[1].startswith('picked'):
                    self.pick_flag = True
            if apt[0] == 'title':
                if self.pick_flag:
                    if apt[1] in self.picks:
                        self.picks[apt[1]] += 1
                    else:
                        self.picks[apt[1]] = 1
                    self.pick_flag = False

    def handle_data(self, data):
        if self.name_flag:
            self.name = data
            self.name_flag = False


def complain(winner, runnerup, history):
    for histo in history:
        if histo[1] != 4:
            print('Invalid number of one and dones')
        if histo[2] != 2:
            print('Invalid number of sweet 16 teams')
        if histo[3] != 1:
            print('Invalid number of elite-8 teams')
    if not winner:
        print('No winner')
    if not runnerup:
        print('No runnerup')
    if len(winner) > 1:
        print('Too many winning teams')
    if len(runnerup) > 1:
        print('Too many runner-up teams')

def sanity_check(picks):
    with open('teams.txt') as ifile:
        allinfo = ifile.read().strip().split('\n')
        sregions = []
        for indx in range(0, 63, 16):
            sregions.append(allinfo[indx:indx+16])
    winner = []
    runnerup = []
    history = []
    for region in sregions:
        histo = [0, 0, 0, 0]
        for entry in region:
            if entry not in picks:
                continue
            tindx = picks[entry]
            if tindx < 4:
                histo[tindx] += 1
            else:
                if tindx == 5:
                    runnerup.append(entry)
                if tindx == 6:
                    winner.append(entry)
        history.append(histo)
    complain(winner, runnerup, history)
    return True


def extract_bracket(in_data):
    req = requests.get(in_data)
    parser = GetBracket()
    parser.feed(req.text)
    retv = {}
    retv['name'] = parser.name
    retv['picks'] = parser.picks
    if not sanity_check(retv['picks']):
        print('%s has problems' % retv['name'])
    return retv


def extract_all():
    out_info = {}
    gdict = get_group()
    for group in os.listdir('members'):
        if group not in gdict:
            print('error: Group %s is invalid' % group)
        fname = 'members%s%s' % (os.sep, group)
        with open(fname, 'r') as fdata:
            ostr = fdata.read()
        glist = []
        for page in ostr.strip().split('\n'):
            indv_info = extract_bracket('%s%s' % (HEADER, page))
            glist.append(indv_info)
        out_info[group] = glist
    with open('group_picks.json', 'w') as outfile:
        json.dump(out_info, outfile)


if __name__ == '__main__':
    extract_all()
