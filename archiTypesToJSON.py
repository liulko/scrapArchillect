import datetime
import os
import time

import archillect
import json


def make_archi_types_json(start_id, end_id):
    to_be_json = list()
    for i in range(start_id, end_id + 1):
        # os.system('clear') if os.name == 'posix' else os.system('cls')
        print(f'interval: {start_id}-{end_id}')
        print(f'work on {i - start_id + 1}/{end_id - start_id + 1}')
        ii = archillect.get_image(i)
        to_be_json.append({
            'id': ii['post_id'],
            'url': ii['url']
        })

    with open(f'out__{start_id}_{end_id}__{datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}.json', 'w') as f:
        json.dump(to_be_json, f)


# make_archi_types_json(archillect.get_last_post_index())
make_archi_types_json(1001, 5000)
