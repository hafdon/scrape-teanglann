import json

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Lexeme", "Present", "Imperative", "Past Habitual", "Past", "Past (Neg)", "Future", "Conditional", sep=", ")

for entry in data:
    word = entry['url']

    past_autonomous = entry['item'].get('past', {}).get('PASSIVE', [])

    present_aut_unmarked = entry['item'].get('present', {}).get('PASSIVE', [])[0].split(' ')[0]
    # Remove trailing exclamation mark if present
    imperative_aut_unmarked = entry['item'].get('imper', {}).get('PASSIVE', [])[0].split('!')[0]
    past_autonomous_unmarked = past_autonomous[0].split(' ')[0] if len(past_autonomous) > 0 else ''
    # Don't split the negative since we want the negative verbal particle as well
    past_autonomous_neg = past_autonomous[2] if len(past_autonomous) > 2 else ''
    past_habitual_aut_unmarked = entry['item'].get('pastConti', {}).get('PASSIVE', [])[0].split(' ')[0]
    future_autonomous = entry['item'].get('future', {}).get('PASSIVE', [])[0].split(' ')[0]
    conditional_autonomous = entry['item'].get('condi', {}).get('PASSIVE', [])[0]



    print(word, present_aut_unmarked, imperative_aut_unmarked,
          past_habitual_aut_unmarked, past_autonomous_unmarked,
          past_autonomous_neg, future_autonomous, conditional_autonomous,
          sep=", ")
