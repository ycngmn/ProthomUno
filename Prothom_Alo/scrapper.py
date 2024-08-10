import requests, re
from bs4 import BeautifulSoup as bs

def extract(url):

    

    soup = bs(requests.get(url).text,'html.parser')

    subtopic = soup.find('h2',class_='uv2z3') # not always available
    subtopic='' if not subtopic else subtopic.text
    topic = soup.find('div',class_='story-title-info BG103').find('a').text
    title = soup.find('h1',class_='IiRps').text
    summary = soup.find('meta',attrs={'name':'description'})['content']

    thumb = soup.find('meta',property='og:image')['content'].split('?')[0]
    scaption = soup.find('picture', class_='qt-image')
    caption_src = scaption.find_next('span') 
    capsrc = caption_src.text if caption_src else None
    if caption_src: caption_src.decompose() # otherwise it's included in caption
    caption = scaption.find_next('figcaption')
    caption = caption.text if caption else '' 
    full_caption = (caption + ' | ' + capsrc) if capsrc else caption

    date = soup.find('div',class_='xuoYp').find('span').text.split(':')[1].strip(" ")
    if ',' in date: # checks if the text also contains hour:second separated by comma
        date = date.split(',')[0]
    tags = soup.find('meta',{'name':'keywords'})['content']


    p = [url,title,summary,topic,subtopic,thumb,tags,date,full_caption]
    return p

def download_thumb(thumb_url):
    with open('assets/images/photo.webp','+wb') as file:
        bytes = requests.get(thumb_url).content
        file.write(bytes)
    return "assets/images/photo.webp"
    