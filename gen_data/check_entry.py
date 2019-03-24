#!/usr/bin/python
# pylint: disable=W0223
"""
Module used to check for invalid entries.
"""
from html.parser import HTMLParser
import requests


class ChkData(HTMLParser):
    """
    Test to see if the groupId passed is used in the html text passed.
    Sets self.retval to True if groupId is used
    """
    def __init__(self, group_id):
        HTMLParser.__init__(self)
        self.retval = False
        self.group_id = 'group?groupID=%s' % group_id

    def handle_starttag(self, tag, attrs):
        for apt in attrs:
            if apt[0] == 'value' or apt[0] == 'href':
                if apt[1] == self.group_id:
                    self.retval = True


def check_entry(page, group_id):
    """
    Do requests call to get html text.  Feed text through the ChkData
    parser.  Return boolean value whether group_id is used in the page or not.
    """
    req = requests.get(page)
    parser = ChkData(group_id)
    parser.feed(req.text)
    return parser.retval
