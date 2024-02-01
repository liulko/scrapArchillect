import requests as r
import bs4
import creds


def get_last_post_index() -> int:
    url = 'https://archillect.com/archive'
    html = r.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    archive = soup.find(id='archive')
    first_a = archive.find_all('a')[0]
    post_id = int(first_a.find(class_="postid").text)
    return post_id


def get_image(post_id: int) -> dict:
    base_url = 'https://archillect.com/'
    post_url = base_url + str(post_id)
    response = r.get(post_url)
    print(f'id {post_id}: {response.status_code} status code')
    while not response.status_code == 200:
        proxy_resp = r.get(creds.proxy_api_address)
        while not proxy_resp.status_code == 200:
            proxy_resp = r.get(creds.proxy_api_address)
        proxy = proxy_resp.text.split(':')
        host = creds.proxy_host
        port = creds.proxy_port
        username = proxy[2]
        password = creds.proxy_password
        proxies = {
            'https': f'http://{username}:{password}@{host}:{port}'
        }
        try:
            response = r.get(post_url, proxies=proxies)
        except Exception as e:
            print(e)
        print(f'id {post_id}: {response.status_code} status code with {username}')

    post_page_html = response.text
    soup = bs4.BeautifulSoup(post_page_html, 'html.parser')
    ii = soup.find(id='ii')
    image_url = ii['src']
    image_name = image_url.split('/')[-1]
    # image_bytes = r.get(ii['src']).content
    image_type = image_name.split('.')[-1]
    return {
        'post_id': post_id,
        'post_url': post_url,
        'url': image_url,
        'name': image_name,
        # 'bytes': image_bytes,
        'image_type': image_type
    }
