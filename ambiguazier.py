import json

targets = ['res_may']

with open('ambig.json', 'r', encoding='utf8') as fp:
    ambig_map = json.load(fp)

for t in targets:
    with open(f'{t}.json', 'r', encoding='utf8') as fp:
        current = json.load(fp)
    for c in current:
        c['Question'] = ambig_map[c['Question']]
    
    with open(f'{t}_ambig.json', 'w', encoding='utf8') as fp:
        json.dump(current, fp, indent=1)