import sys
import json
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


with open('result.json', 'r', encoding='utf8') as json_file:
    jdata = json.load(json_file, encoding='utf-8')
print(jdata)
print(len(jdata['Mad_as_a_March_Llama'].keys()))
