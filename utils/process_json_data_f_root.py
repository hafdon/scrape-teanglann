import json

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    word = entry['url']
    verbal_noun = entry['item'].get('verbal_noun')
    past_singular = entry['item'].get('past', {}).get('SINGULAR', [])
    future = entry['item'].get('future', {}).get('SINGULAR', [])[0].split(' ')[0]
    # Process or print the data as needed

    future_analytic = entry['item'].get('future', {}).get('SINGULAR', [])[0].split(' ')[0]
    future_syn_1pl = entry['item'].get('future', {}).get('PLURAL', [])[0].split(' ')[0]
    future_autonomous = entry['item'].get('future', {}).get('PASSIVE', [])[0].split(' ')[0]

    print(future_analytic, future_syn_1pl, future_autonomous)




