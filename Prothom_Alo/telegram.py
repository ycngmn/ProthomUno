import requests, json, os


bot_token = "" # https://t.me/botfather
channel_id = '' # replace with yours

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
    title = fetch_data[-1]


    media = []
    files = {}

    for i in range(len(image_keys)): 
        file_path = f'assets/images/Glimpses/{i}.jpg'
        caption = f"{caption_keys[i]}|{source_keys[i]}"

        # Unique key for each file
        file_key = f'photo_{i}'
        media.append({
            'type': 'photo',
            'media': f'attach://{file_key}',
            'caption': caption,
        })

        with open(file_path, 'rb') as photo_file:
            files[file_key] = (file_key, photo_file.read())

    # Sending the POST request
    url = f'https://api.telegram.org/bot{bot_token}/sendMediaGroup'
    response = requests.post(url, data={
        'chat_id': channel_id,
        'media': json.dumps(media)},  # Convert the media list to JSON
    files=files)

    if response.status_code == 200:
         url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
         response = requests.post(url, data={
                'chat_id': channel_id,
                'text': title,
            })
         print("Telegram posted multiple images as a group!")
        
         message_id = response.json().get('result', {}).get('message_id')
         if message_id:
            # Pin the message
            pin_url = f'https://api.telegram.org/bot{bot_token}/pinChatMessage'
            requests.post(pin_url, data={
                'chat_id': channel_id,
                'message_id': message_id,
                'disable_notification': True})

    else:
        print(f"Error posting images to Telegram: {response.text}")