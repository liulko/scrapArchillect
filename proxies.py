import random
import creds

PROXY_LIST = open('ips-datacenter_proxy12026-11-19T09_01_34.331Z.txt', 'r').read().split('\n')

def get_proxy():
    proxy = PROXY_LIST[random.randrange(len(PROXY_LIST))]
    host = creds.proxy_host
    port = creds.proxy_port
    username = creds.proxy_username + proxy
    password = creds.proxy_password
    return {
        'https': f'http://{username}:{password}@{host}:{port}'
    }