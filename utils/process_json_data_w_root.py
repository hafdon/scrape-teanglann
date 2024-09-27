import json

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    word = entry['url']
    verbal_noun = entry['item'].get('verbal_noun')
    past_singular = entry['item'].get('past', {}).get('SINGULAR', [])
    future = entry['item'].get('future', {}).get('SINGULAR', [])[0].split(' ')[0]
    # Process or print the data as needed

    present_autonomous = entry['item'].get('present', {}).get('PASSIVE', [])[0].split(' ')[0]
    imperative_autonomous = entry['item'].get('imper', {}).get('PASSIVE', [])[0].split(' ')[0]
    past_habitual_autonomous = entry['item'].get('pastConti', {}).get('PASSIVE', [])[0].split(' ')[0]
    past_habitual_syn_2sg = entry['item'].get('pastConti', {}).get('SINGULAR', [])[3].split(' ')[0]

    print(present_autonomous, imperative_autonomous, past_habitual_autonomous, past_habitual_syn_2sg)
