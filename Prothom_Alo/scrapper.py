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
    caption = soup.find('figcaption',class_='story-element-image-caption custom-gallery-image')
    if caption:
        capsrc = caption.find('span')
        if capsrc:
            caption_source = capsrc.text
            capsrc.decompose()
        else: caption_source = None
        caption = caption.text if caption else None
        full_caption = (caption + ' | ' + caption_source) if caption_source else caption
    else:
        full_caption = None

    date = soup.find('div',class_='xuoYp').find('span').text.split(':')[1].strip(" ")
    if ',' in date: # checks if the text also contains hour:second separated by comma
        date = date.split(',')[0]
    tags = soup.find('meta',{'name':'keywords'})['content']


    return (url,title,summary,topic,subtopic,thumb,tags,date,full_caption)

def extract_glimpses(json_data):

    json_data = requests.get(json_data).text

    image_pattern = re.compile(r'"image-s3-key":\s*"([^"]*)"', re.DOTALL)
    caption_pattern = re.compile(r'"image-attribution":\s*"([^"]*)".*?"title":\s*"([^"]*)"', re.DOTALL)
    source_pattern = re.compile(r'"image-attribution":\s*"([^"]*)"', re.DOTALL)
    title_pattern = re.compile(r'"metadata"\s*:\s*{\s*"[^"]*"\s*:\s*{[^}]*"title"\s*:\s*"([^"]*)"', re.DOTALL)


    base_url = "https://images.prothomalo.com/"
    image_keys = image_pattern.findall(json_data)
    image_keys = [base_url+a.replace('\\u002F','/') for a in image_keys][:-1]

    caption_keys = [match.group(2) for match in caption_pattern.finditer(json_data)]

    source_keys = source_pattern.findall(json_data)

    title = title_pattern.search(json_data).group(1)

    return (image_keys,caption_keys,source_keys,title)


def download_thumb(thumb_url):
    with open('assets/images/photo.webp','+wb') as file:
        bytes = requests.get(thumb_url).content
        file.write(bytes)
    return "assets/images/photo.webp"
    