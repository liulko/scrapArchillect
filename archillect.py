import requests as r
import bs4


def get_max_index() -> int:
    url = 'https://archillect.com/archive'
    html = r.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    archive = soup.find(id='archive')
    first_a = archive.find_all('a')[0]
    post_id = first_a.find(class_="postid").text
    return post_id


def get_image(post_id: int) -> dict:
    base_url = 'https://archillect.com/'
    post_page_html = r.get(f'{base_url}{post_id}').text
    soup = bs4.BeautifulSoup(post_page_html, 'html.parser')
    ii = soup.find(id='ii')
    image_url = ii['src']
    image_name = image_url.split('/')[-1]
    image_bytes = r.get(ii['src']).content

    return {
        'bytes': image_bytes,
        'name': image_name
    }


last_id = get_max_index()
image = get_image(last_id)
with open(f'{image["name"]}', 'wb') as f:
    f.write(image['bytes'])
    f.close()
