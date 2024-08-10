from twikit import Client

client = Client()

""" # convert chrome cookies to support twikit 
def convert_cookies(): 
    
    import json

    with open(r'Prothom_Alo\assets\cookie.json', 'r') as file: 
        data = json.load(file)

    result = {}
    for item in data:
        name = item.get("name")
        value = item.get("value")
        if name and value:
            result[name] = value

    with open(r'Prothom_Alo\assets\cookie.json', 'w') as file:
        json.dump(result, file, indent=4)
"""


async def main(fetch_data):
    
    client.load_cookies(r'assets/cookie.json')

    cap = fetch_data[2]
    tags = " ".join(['#'+tag.replace(' ','_') for tag in fetch_data[6].split(',')])

    

    media_path = r'assets/images/inserted.jpeg'
    media_id = [await client.upload_media(media_path)]

    # Create a tweet with the provided text and attached media
    a = await client.create_tweet(
    text=cap+'\n\n'+tags,
    media_ids=media_id
    )
    
    print("Tweeted  !",a.full_text.split(' ')[-1])

