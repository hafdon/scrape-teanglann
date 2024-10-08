"""
This script processes the JSON data from the Teanglann scraper and extracts the conditional forms of the root verb.
"""

import json

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print()

for entry in data:
    word = entry['url']

    conditional_analytic = entry['item'].get('condi', {}).get('SINGULAR', [])[6].split(' ')[0]
    conditional_synthetic_1sg = entry['item'].get('condi', {}).get('SINGULAR', [])[0]
    conditional_synthetic_2sg = entry['item'].get('condi', {}).get('SINGULAR', [])[3]
    conditional_synthetic_1pl = entry['item'].get('condi', {}).get('PLURAL', [])[0]
    conditional_synthetic_3pl = entry['item'].get('condi', {}).get('PLURAL', [])[9]
    conditional_autonomous = entry['item'].get('condi', {}).get('PASSIVE', [])[0]


    print(conditional_analytic, conditional_synthetic_1sg, conditional_synthetic_2sg, conditional_synthetic_1pl, conditional_synthetic_3pl, conditional_autonomous)