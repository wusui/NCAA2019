#!/usr/bin/python
"""
Ini file reader
"""
from configparser import ConfigParser


def get_group():
    """
    Extract the info from groups.ini and save the result in a dictionary.

    Entries in the extracted dictionary will be:
        <group name> : <groupID>

    Where the <group name> value has underscores replacing blanks.

    Returns the data in the groups.ini file.
    """
    retval = {}
    ginfo = ConfigParser()
    ginfo.read("groups.ini")
    for name in ginfo.sections():
        nname = '_'.join(name.strip().split(' '))
        retval[nname] = ginfo.get(name, 'groupID')
    return retval
