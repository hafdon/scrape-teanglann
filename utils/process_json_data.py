import json

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    word = entry['url']
    verbal_noun = entry['item'].get('verbal_noun')
    past_singular = entry['item'].get('past', {}).get('SINGULAR', [])
    future = entry['item'].get('future', {}).get('SINGULAR', [])[0].split(' ')[0]
    # Process or print the data as needed
    future_split = ""
    # if future.endswith('faidh'):
    #     future_split = future.split('faidh')[0]
    #     print( f"{future_split}-[1b]", end="\t")
    # elif future.endswith('fidh'):
    #     future_split = future.split('fidh')[0]
    #     print(f"{future_split}-[1s]", end="\t")
    # elif future.endswith('óidh'):
    #     future_split = future.split('óidh')[0]
    #     print(f"{future_split}-[2b]", end="\t")
    # elif future.endswith('eoidh'):
    #     future_split = future.split('eoidh')[0]
    #     print(f"{future_split}-[2s]", end="\t")

    present = entry['item'].get('present', {}).get('SINGULAR', [])[3].split(' ')[0]
    present_split = ""
    if present.endswith('eann'):
        present_split = present.split('eann')[0]
        print(f"{present_split}-[1s]", end =  "\t")
    elif present.endswith('ann'):
        present_split = present.split('ann')[0]
        print( f"{present_split}-[1b]", end =  "\t")
    elif present.endswith('aíonn'):
        present_split = present.split('aíonn')[0]
        print(f"{present_split}-[2b]", end =  "\t")
    elif present.endswith('íonn'):
        present_split = present.split('íonn')[0]
        print(f"{present_split}-[2s]", end =  "\t")

    # print(present_split == future_split)
    print()
