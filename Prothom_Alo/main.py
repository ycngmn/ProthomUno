import requests, re, traceback, time
import sqlite3
import image, facebook, telegram
from scrapper import extract, extract_glimpses

db = sqlite3.connect('assets/storage.db', check_same_thread=False)
cu = db.cursor()
cu.execute("CREATE TABLE IF NOT EXISTS news (id INT, url TEXT)")
db.commit()


while True:

    fetch = requests.get('https://www.prothomalo.com/collection/latest')
    fetch.raise_for_status()
    pattern = r'<h3 class="headline-title   _1d6-d">\s*<a[^>]*href="([^"]*)"'
    urls = re.findall(pattern, fetch.text)[:6]

    get_dbs = cu.execute("SELECT url FROM news ORDER BY id DESC LIMIT 6").fetchall()
    get_dbs = [i[0] for i in get_dbs]
    
    for url in urls:
         if url not in get_dbs:
            print("New article found ..!", url)

            get_id = cu.execute("SELECT MAX(id) FROM news").fetchone()[0]
        
            cu.execute(f"INSERT INTO news VALUES({get_id+1}, '{url}')")
            db.commit()
        
    # try-exeption to ignore the errors if occurs. 
            try: 
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

            except Exception:
                    traceback.print_exc()
                    print("\nException passed. Waiting for new articles..")
    cu.execute("DELETE FROM news WHERE id NOT IN (SELECT id FROM news ORDER BY id DESC LIMIT 6)")
    db.commit() 
    
    time.sleep(60)
