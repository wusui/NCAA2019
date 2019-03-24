import sys
import codecs
import json
import os
from get_results import get_results

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

POINTS = [0, 10, 30, 70, 150, 310, 630]


def scorekeep(plr, results):
    retv = [0, 0]
    for teamn in plr['picks']:
        realp = min(plr['picks'][teamn], results[teamn]['wins'])
        possp = realp
        if results[teamn]['alive']:
            possp = plr['picks'][teamn]
        retv[0] += POINTS[realp]
        retv[1] += POINTS[possp]
    return retv

def readm():
    jname = '..' +os.sep + 'gen_data' + os.sep + 'group_picks.json'  
    with open(jname, 'r', encoding='utf8') as json_file:
        jdata = json.load(json_file, encoding='utf-8')
    return jdata

def scorem(results, jdata):
    retv = {}
    for entry in jdata:
        bb_group = []
        for player in jdata[entry]:
            result = scorekeep(player, results)
            player['score'] = result[0]
            player['best_poss'] = result[1]
            bb_group.append(player)
        sorted_list= sorted(bb_group, reverse=True,
            key= lambda item: (item['score'], item['best_poss']))
        retv[entry] = sorted_list
    return retv

if __name__ == "__main__":
    results = scorem(get_results(), readm())
    for group in results:
        print(group)
        for bracket in results[group]:
            print(bracket['name'], bracket['score'], bracket['best_poss'])
