import requests, re, traceback
import sqlite3
import image, facebook, telegram
from scrapper import extract


db = sqlite3.connect('assets/storage.db', check_same_thread=False)
cu = db.cursor()
cu.execute("CREATE TABLE IF NOT EXISTS news (id INT, url TEXT)")
db.commit()


while True:
    # Get the last entry to the database
    get_db = cu.execute("SELECT url FROM news ORDER BY id DESC LIMIT 1").fetchone()
    if get_db: get_db = get_db[0]

    # Get the latest article URL
    fetch = requests.get('https://www.prothomalo.com/collection/latest')
    fetch.raise_for_status()
    pattern = r'<div\s+class="stKlc">.*?<a[^>]*\s+href="([^"]+)"'
    url = re.search(pattern, fetch.text).group(1)

    if not url == get_db:
        try:
            print("New article found  ..!", url)
            get_id = cu.execute("SELECT id FROM news ORDER BY id DESC LIMIT 1").fetchone()
            if not get_id: 
                get_id = 0
            else: 
                get_id = get_id[0]
                cu.execute(f"DELETE FROM news WHERE id={get_id}")

            cu.execute(f"INSERT INTO news VALUES({get_id + 1}, '{url}')")
            db.commit()

          
            fetch_data = extract(url)

            image.add_text(fetch_data)
            facebook.post(fetch_data)
            telegram.post(fetch_data)
            
            print('Waiting for new articles..')
        except Exception:
            traceback.print_exc()
            print("\nException passed. Waiting for new articles..")
    

