import tweepy

def post_tweet(fetch_data):

    api_key = ''
    api_secret = ''
    access_token = ''
    access_token_secret = ''
    bearer_token= ''

    auth = tweepy.OAuth1UserHandler(api_key, api_secret,access_token,
            access_token_secret) 

    client_v1 = tweepy.API(auth)
    client_v2 = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret)

    cap = fetch_data[2]
    tags = " ".join(['#'+tag.replace(' ','_') for tag in fetch_data[6].split(',')])
    media_path = r'Prothom_Alo/assets/images/inserted.jpeg'
    media = client_v1.media_upload(filename=media_path)
    response = client_v2.create_tweet(text=cap+'\n\n'+tags, media_ids=[media.media_id])
    tweet_url = response.data['text'].split(' ')[-1].strip("' ")
    print("Tweeted  !", tweet_url)