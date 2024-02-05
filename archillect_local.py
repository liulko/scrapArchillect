import json
import random

import requests as r
import bs4
import creds

ARCHI_ARCHIVE = [i for i in json.loads(open('archillect_final_dict.json', 'rb').read())]
print(len(ARCHI_ARCHIVE))


def get_last_post_index() -> int:
    return len(ARCHI_ARCHIVE)


def get_image(post_id: int) -> dict:
    image_url = ARCHI_ARCHIVE[post_id - 1]['url']
    image_name = image_url.split('/')[-1]
    image_type = image_name.split('.')[-1]
    post_url = f'https://archillect.com/{post_id}'
    return {
        'post_id': post_id,
        'post_url': post_url,
        'url': image_url,
        'name': image_name,
        'image_type': image_type
    }
