import requests


bot_token = ''
channel_id = ''

def post(fetch_data):
    
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

    caption = fetch_data[2] + ' ' + f"<a href='{fetch_data[0]}'>বিস্তারিত...</a>"
    
    with open(r'assets/images/inserted.jpeg', 'rb') as photo_file:
    
        files = {'photo': photo_file}
        data = {
            'chat_id': channel_id,
            'caption': caption,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True  # Disable web preview
        }
        requests.post(url, data=data, files=files)
    
    print("Telegram posted  !")

def post_multiple_images_as_group(fetch_data: list) -> None:

    image_keys = fetch_data[0]
    caption_keys = fetch_data[1] 
    source_keys = fetch_data[2]

    image_captions = [(f'assets/images/Glimpses/{i}.jpg', caption_keys[i] +'|'+ source_keys[i]) for i in range(len(image_keys))]
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMediaGroup'

    media = []
    for image_path, caption in image_captions:
        with open(image_path, 'rb') as photo_file:
            media.append({
                'type': 'photo',
                'media': photo_file,
                'caption': caption,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True  # Disable web preview
            })
    
    data = {
        'chat_id': channel_id,
        'media': media
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Telegram posted multiple images as a group!")
    else:
        print(f"Error posting images to Telegram: {response.text}")
