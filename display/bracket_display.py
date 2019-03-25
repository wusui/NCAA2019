#!/usr/bin/python
"""
Generate html pages for all group being checked.
"""
import os
from configparser import ConfigParser
import sys
import json
import codecs
from gen_records import gen_records
from gen_html import gen_html


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def bracket_display():
    """
    Generate html pages for all groups.  Group names are extracted from the
    section names in ../gen_data/groups.ini and are updated using the data
    in ../figure_future/result.json
    """
    with open('abbrevs.txt', 'r') as afile:
        team_nms = afile.readlines()
    team_nms = [x.strip() for x in team_nms]
    rem_json = '..%sfigure_future%sresult.json' % (os.sep, os.sep)
    with open(rem_json, 'r', encoding='utf8') as json_file:
        jdata = json.load(json_file, encoding='utf-8')
    ginfo = ConfigParser()
    ginfo.read("..%sgen_data%sgroups.ini" % (os.sep, os.sep))
    for name in ginfo.sections():
        nname = '_'.join(name.strip().split(' '))
        rec_list = gen_records(jdata[nname])
        gen_html(name, rec_list, team_nms)


if __name__ == "__main__":
    bracket_display()
