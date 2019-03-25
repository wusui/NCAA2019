#!/usr/bin/python
"""
Html page generator
"""
from gen_table_line import gen_table_header
from gen_table_line import gen_table_row


def gen_html(name, rec_list, abbrevs):
    """
    Generate an Html page for a pool.
    """
    with open('header.txt', 'r') as fdata:
        ostr = fdata.read()
    nhead = ostr % (name, name)
    with open('trailer.txt', 'r') as fdata:
        trailer = fdata.read()
    oname = '_'.join(name.split(' '))
    with open(oname + '.html', 'w', encoding='utf8') as odata:
        odata.write(nhead)
        headr = gen_table_header(abbrevs)
        odata.write(headr)
        total = 0.0
        for entry in rec_list:
            total += entry['percentage']
            dline = gen_table_row(entry, abbrevs)
            odata.write(dline)
        print(total)
        odata.write(trailer)
