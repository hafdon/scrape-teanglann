import json

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print()

for entry in data:
    word = entry['url']
    # Process or print the data as needed

    present_analytic = entry['item'].get('present', {}).get('SINGULAR', [])[3].split(' ')[0]
    present_syn_1sg = entry['item'].get('present', {}).get('SINGULAR', [])[0].split(' ')[0]
    present_syn_1pl = entry['item'].get('present', {}).get('PLURAL', [])[0].split(' ')[0]
    imperative_analytic = entry['item'].get('imper', {}).get('SINGULAR', [])[4].split(' ')[0]

    # Prevent some index errors by checking the length of the list
    past_plural = entry['item'].get('past', {}).get('PLURAL', [])
    past_autonomous = entry['item'].get('past', {}).get('PASSIVE', [])

    past_syn_1pl = past_plural[0].split(' ')[0] if len(past_plural) > 0 else ''
    past_syn_3pl = past_plural[12].split(' ')[0] if len(past_plural) > 12 else ''
    past_autonomous_unmarked = past_autonomous[0].split(' ')[0] if len(past_autonomous) > 0 else ''
    # Don't split the negative since we want the negative verbal particle as well
    past_autonomous_neg = past_autonomous[2] if len(past_autonomous) > 2 else ''
    past_habitual_analytic = entry['item'].get('pastConti', {}).get('SINGULAR', [])[6].split(' ')[0]

    print(present_analytic, present_syn_1sg, present_syn_1pl, imperative_analytic,
          past_syn_1pl, past_syn_3pl, past_autonomous_unmarked, past_autonomous_neg, past_habitual_analytic, sep=",")

    # print( past_syn_1pl, past_syn_3pl, past_autonomous_unmarked, past_autonomous_neg, past_habitual_analytic, sep=",")
