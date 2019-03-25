def wrapper(field, wrap_txt):
    answer = "<%s>" % wrap_txt
    answer += field
    answer += "</%s>" % wrap_txt
    return answer

def gen_head_sect(headings):
    parts = []
    for txtfld in headings:
        sects = txtfld.split(' ')
        if len(sects) == 1:
            parts.append(wrapper(txtfld, 'th'))
        else:
            ostr = ''
            for nparts in sects:
                ostr += wrapper(nparts, 'div')
            parts.append(wrapper(ostr, 'th'))
    mstr = ''
    for part in parts:
        mstr += part
    return mstr

def gen_table_header(abbrev):
    headings = ['NAME', 'Winning Outcomes', 'Percentage']
    ostrv = gen_head_sect(headings)
    evens = abbrev[::2]
    odds = abbrev[1:][::2]
    matches = []
    for cnt, oddp in enumerate(odds):
        matches.append(evens[cnt]+' '+oddp)
    ostrv += gen_head_sect(matches)
    return wrapper(ostrv, 'tr')

def needed_fields(dist_info, abbrev):
    style = []
    pickx = []
    evens = abbrev[::2]
    odds = abbrev[1:][::2]
    for indx, dist_infp in enumerate(dist_info):
        if dist_infp[0] > dist_infp[1]:
            pickx.append(evens[indx])
        if dist_infp[1] > dist_infp[0]:
            pickx.append(odds[indx])
        if dist_infp[1] == dist_infp[0]:
            pickx.append('*')
            style.append("#ffffff")
            continue
        if dist_infp[1] == 0 or dist_infp[0] == 0:
            style.append("#000000;color:#ffffff")
            continue
        cstyle = color_me(dist_infp)
        style.append(cstyle)
    retv = ''
    for indx, value in enumerate(pickx):
        retv += '<td style="background-color:'
        retv += style[indx]
        retv += '">'
        retv += value
        retv += '</td>'
    return retv

def color_me(dist_infp):
    total = sum(dist_infp)
    high = max(dist_infp)
    compv = high * 1024
    compv /= total
    compv -= 511.5
    color = int(compv)
    if color < 0:
        color = 0
    if color > 511:
        color = 511
    greenv = 255
    if color < 256:
        redv = color
    else:
        redv = 255
        xtra = color - 256
        greenv -= xtra
    cstyle = '#'
    cstyle += "{:02X}".format(redv)
    cstyle += "{:02X}".format(greenv)
    cstyle += "00"
    return cstyle


def gen_table_row(record, abbrevs):
    ostr = wrapper(record['name'], 'td')
    ostr += wrapper(str(record['winning_outcomes']), 'td')
    pct = "{:7.5f}".format(record['percentage'])
    ostr += wrapper(pct, 'td')
    ostr += needed_fields(record['next_round'], abbrevs)
    return wrapper(ostr, 'tr')
