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