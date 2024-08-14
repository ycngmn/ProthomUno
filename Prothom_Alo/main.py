import requests, re, traceback, time
import sqlite3
import image, facebook, telegram
from scrapper import extract, extract_glimpses
import threading

db = sqlite3.connect('assets/storage.db', check_same_thread=False)
cu = db.cursor()
cu.execute("CREATE TABLE IF NOT EXISTS news (id INT, url TEXT)")
db.commit()

def scrap_url(queue):
    while True:
        get_db = cu.execute("SELECT url FROM news").fetchone()
        if get_db: get_db = get_db[0]
        fetch = requests.get('https://www.prothomalo.com/collection/latest')
        fetch.raise_for_status()
        
        pattern = r'<div\s+class="stKlc">.*?<a[^>]*\s+href="([^"]+)"'
        url = re.search(pattern, fetch.text).group(1)

        if not url == get_db:
            print("New article found ..!", url)
            queue.append(url)
            
            cu.execute(f"DELETE FROM news WHERE id=0")
            db.commit() 
            cu.execute(f"INSERT INTO news VALUES(0, '{url}')")
            db.commit()
            
        else:
             time.sleep(5)

queue = []
scrap_thread = threading.Thread(target=scrap_url, args=(queue,))
scrap_thread.start()

while True:
    
    # try-exeption to ignore the errors if occurs. 
    try: 
        if queue:
            url = queue.pop(0)
            if '/photo/' in url: # if a photo article, post all the photos with captions
                fetch_data = extract_glimpses(url)
                facebook.multi_posting(fetch_data)
                telegram.post_multiple_images_as_group(fetch_data)
                print('Waiting for new articles..')
                continue

            fetch_data = extract(url)

            image.add_text(fetch_data)
            facebook.post(fetch_data)
            telegram.post(fetch_data)
            
            print('Waiting for new articles..')
        else:
             time.sleep(4)

    except Exception:
            traceback.print_exc()
            print("\nException passed. Waiting for new articles..")
    

