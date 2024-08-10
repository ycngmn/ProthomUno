import requests, re
import sqlite3
import os ,time
import image, tweet
from scrapper import extract
import traceback
import asyncio


db = sqlite3.connect('assets/storage.db',check_same_thread=False)
cu = db.cursor()
cu.execute("CREATE TABLE IF NOT EXISTS news (id INT, url TEXT)")
db.commit()



while True:

    
    # Get the last entry to the databse
    get_db = cu.execute("SELECT url FROM news ORDER BY id DESC LIMIT 1").fetchone()
    if get_db: get_db = get_db[0]

    # Get latest article url
    fetch = requests.get('https://www.prothomalo.com/collection/latest')
    fetch.raise_for_status()
    pattern = r'<div\s+class="stKlc">.*?<a[^>]*\s+href="([^"]+)"'
    url = re.search(pattern,fetch.text).group(1)
    
    if not url == get_db:
        try:
            print("New article found  ..!",url)
            get_id = cu.execute("SELECT id FROM news ORDER BY id DESC LIMIT 1").fetchone()
            # if the database is still vierge..
            if not get_id: get_id = 0
            else: 
                get_id = get_id[0]
                cu.execute(f"DELETE FROM news WHERE id={get_id}")

            cu.execute(f"INSERT INTO news VALUES({get_id+1},'{url}')")
            db.commit()
            fetch = extract(url)
            image.add_text(fetch)
            asyncio.run(tweet.main(fetch))
            print('Waiting for newses..')
        except Exception:
            print("Exception passed. Waiting for new articles..")
            traceback.print_exc()
    else:
        time.sleep(45)



