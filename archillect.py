import requests as r
import bs4


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
    post_page_html = r.get(post_url).text
    soup = bs4.BeautifulSoup(post_page_html, 'html.parser')
    ii = soup.find(id='ii')
    image_url = ii['src']
    image_name = image_url.split('/')[-1]
    # image_bytes = r.get(ii['src']).content
    return {
        'post_id': post_id,
        'post_url': post_url,
        'url': image_url,
        'name': image_name,
        # 'bytes': image_bytes
    }
