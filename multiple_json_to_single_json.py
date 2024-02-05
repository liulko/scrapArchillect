import json
import os
arr = os.listdir('outputs')

archillect_final_dict = list()

for i in arr:
    print(i)
    tmp_dict = json.loads(open(f'outputs/{i}', 'rb').read())
    print(type(tmp_dict))
    print(tmp_dict[0])
    for j in tmp_dict:
        archillect_final_dict.append(j)

archillect_final_dict = sorted(archillect_final_dict, key=lambda d: d['id'])

with open('archillect_final_dict.json', 'w') as f:
    json.dump(archillect_final_dict, f)

