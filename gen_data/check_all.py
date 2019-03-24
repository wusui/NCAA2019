#!/usr/bin/python
"""
Check members files
"""
import os
from get_group import get_group
from check_entry import check_entry


HEADER = 'http://fantasy.espn.com/tournament-challenge-bracket/'
HEADER += '2019/en/entry?entryID='


def check_all():
    """
    Look through all the files in members directory

    Call check_entry to see if each line of each file is a readable url
    that contains the groupID corresponding to this entry.

    Print error messages if invalid entries are found.
    """
    gdict = get_group()
    for group in os.listdir('members'):
        if group not in gdict:
            print('error: Group %s is invalid' % group)
        fname = 'members%s%s' % (os.sep, group)
        with open(fname, 'r') as fdata:
            ostr = fdata.read()
        for page in ostr.strip().split('\n'):
            if not check_entry(HEADER + page, gdict[group]):
                print('error: page %s invalid for groupID %s' % (page,
                                                                 gdict[group]))


if __name__ == '__main__':
    check_all()
