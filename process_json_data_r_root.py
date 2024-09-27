import json

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    word = entry['url']
    verbal_noun = entry['item'].get('verbal_noun')
    past_singular = entry['item'].get('past', {}).get('SINGULAR', [])
    future = entry['item'].get('future', {}).get('SINGULAR', [])[0].split(' ')[0]
    # Process or print the data as needed

    present_analytic = entry['item'].get('present', {}).get('SINGULAR', [])[3].split(' ')[0]
    present_syn_1sg = entry['item'].get('present', {}).get('SINGULAR', [])[0].split(' ')[0]
    present_syn_1pl = entry['item'].get('present', {}).get('PLURAL', [])[0].split(' ')[0]
    imperative_analytic = entry['item'].get('imper', {}).get('SINGULAR', [])[4].split(' ')[0]

    print(present_analytic, present_syn_1sg, present_syn_1pl, imperative_analytic)