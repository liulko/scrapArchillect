import datetime
import os
import time

import archillect
import json


def make_archi_types_json(max_id):
    to_be_json = list()
    for i in range(1, max_id + 1):
        # os.system('clear') if os.name == 'posix' else os.system('cls')
        print(f'work on {i}/{max_id}')
        ii = archillect.get_image(i)
        to_be_json.append({
            'id': ii['post_id'],
            'url': ii['url']
        })

    with open(f'out__{datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}.json', 'w') as f:
        json.dump(to_be_json, f)


# make_archi_types_json(archillect.get_last_post_index())
make_archi_types_json(5000)
