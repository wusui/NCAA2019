import json
import copy
from get_results import get_survivors
from get_results import get_results
from scorem import readm
from scorem import scorem

def gen_numvec(numb, length):
    ovec = []
    for indx in range(0, length):
        ovec.append(numb%2)
        numb //= 2
    return ovec
        

def assign_wl_vals(teams, picker):
    if len(teams) == 1:
        return []
    evens = teams[::2]
    odds = teams[1:][::2]
    retv = []
    for count in range(0,len(evens)):
        if picker[count] == 1:
            retv.append(odds[count])
        else:
            retv.append(evens[count])
    return retv


def gen_future(numb, size, teamvec):
    result = []
    picker = gen_numvec(numb, size)
    teams = teamvec.copy()
    while(teams):
        teams = assign_wl_vals(teams,picker)
        result.extend(teams)
        picker = picker[len(teams):] 
    return result

def loc_update(rslts, picks):
    for entry in picks:
        rslts[entry]['wins'] += 1
    return rslts


def gen_histo(twoexp):
    lsize = (twoexp + 1) // 2
    if lsize == 2:
        lsize = 3
    retv = []
    for cnt in range(0, lsize):
        retv.append([0,0])
    return retv


def gupdate(fields, indx):
    tnumb = indx
    for gm in range(0, len(fields)):
        val = tnumb % 2
        tnumb //= 2
        fields[gm][val] += 1
    return fields

def gen_outcomes():
    base_teams = get_survivors()
    twoexp = len(base_teams) - 1
    base_peeps = readm()
    retv = {}
    base_results = get_results()
    pinfo = scorem(base_results, base_peeps)
    for group in pinfo:
        retv[group] = {}
    for indx in range(0, 2**twoexp):
        picks = gen_future(indx, twoexp, base_teams)
        temp_res = copy.deepcopy(base_results)
        rslts = loc_update(temp_res, picks)
        pinfo = scorem(rslts, base_peeps)
        for group in pinfo:
            prev = 0
            wlist = []
            for bracket in pinfo[group]:
                if bracket['score'] < prev:
                    break
                wlist.append(bracket['name'])
                prev = bracket['score']
            if indx % 100 == 0:
                print(indx)
            for name in wlist:
                if name not in retv[group]:
                    retv[group][name] = []
                    retv[group][name].append(0)
                    retv[group][name].append(gen_histo(twoexp))
                retv[group][name][0] += 1/len(wlist)
                retv[group][name][1] = gupdate(retv[group][name][1], indx)
    return retv

if __name__ == "__main__":
    all_data = gen_outcomes()
    with open("result.json","w", encoding='utf-8') as jsonfile:
        json.dump(all_data,jsonfile,ensure_ascii=False)
