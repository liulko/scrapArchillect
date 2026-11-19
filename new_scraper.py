import sqlite3
import requests
import bs4
from proxies import get_proxy
# Підключаємося до бази даних (якщо файлу немає, він створиться автоматично)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Створюємо таблицю.
# id тепер PRIMARY KEY, але ми можемо передавати його вручну.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY,
        post_url TEXT,
        image_url TEXT,
        image_name TEXT,
        image_type TEXT
    )
""")
conn.commit()

def write_to_database(post_id, post_url, image_url, image_name, image_type):
    try:
        cursor.execute("""
                       INSERT INTO links (id, post_url, image_url, image_name, image_type)
                       VALUES (?, ?, ?, ?, ?)
                       """, (post_id, post_url, image_url, image_name, image_type))
        conn.commit()
        print(f"Успішно додано запис з ID: {post_id}")
    except sqlite3.IntegrityError:
        print(f"Помилка: ID {post_id} вже існує в базі!")

# --- 2. ЯК ДІЗНАТИСЯ ОСТАННІЙ (МАКСИМАЛЬНИЙ) ID У БАЗІ ---
# Це потрібно, якщо вам треба знати, який ID був останнім,
# щоб призначити наступний (+1) для нового запису.
cursor.execute("SELECT MAX(id) FROM links")
result = cursor.fetchone()[0]

# Якщо таблиця порожня, MAX(id) поверне None, тому ставимо 0 за замовчуванням
last_id = result if result is not None else 0
next_id = last_id + 1
max_id = 410187

print(f"Останній існуючий ID у базі: {last_id}")
print(f"Рекомендований наступний ID: {next_id}")

# Завжди закриваємо з'єднання після завершення роботи

def get_image_info(post_id: int):
    base_url = 'https://archillect.com/'
    archillect_achive_url = base_url + str(post_id)
    response = requests.get(archillect_achive_url)
    print(f'id {post_id}: {response.status_code} status code')
    while not response.status_code == 200:
        if response.status_code == 504:
            return {
                'post_id': post_id,
                'url': False
            }
        proxies = get_proxy()
        try:
            response = requests.get(archillect_achive_url, proxies=proxies)
        except Exception as e:
            print(e)
        print(f'id {post_id}: {response.status_code} status code with proxy')

    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    try:
        ii = soup.find(id='ii')
        image_url = ii['src']
        image_name = image_url.split('/')[-1]
        # image_bytes = r.get(ii['src']).content
        image_type = image_name.split('.')[-1]
        return post_id, archillect_achive_url, image_url, image_name, image_type

    except:
        print( {
            'post_id': post_id,
            'url': False
        })

for i in range(next_id, max_id):
    a,b,c,d,e = get_image_info(i)
    write_to_database(a,b,c,d,e)
conn.close()