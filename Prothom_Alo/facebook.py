import requests, json, os

page_id = "" # replace with yours
access_token = "" # https://developers.facebook.com/

def post(fetch_data):

    
    '''

    To generate long lived access token (60 days)

    https://graph.facebook.com/v20.0/oauth/access_token?
    grant_type=fb_exchange_token&
    client_id=YOUR_APP_ID&
    client_secret=YOUR_APP_SECRET&
    fb_exchange_token=SHORT_LIVED_USER_ACCESS_TOKEN

    '''

    upload_url = f"https://graph.facebook.com/v20.0/{page_id}/photos"

    with open('assets/images/inserted.jpeg', 'rb') as photo_file:
        
        photo_data = {
            'caption':fetch_data[2],
            'access_token': access_token,}
        
        files = {
            'source': photo_file,}

        photo_response = requests.post(upload_url, data=photo_data, files=files)


    if photo_response.status_code == 200:
    
        photo_id = photo_response.json().get('id')
        print("Post successfully created")

        # Add a comment to the post
        comment_url = f"https://graph.facebook.com/v20.0/{photo_id}/comments"

        comment_data = {
            'message': fetch_data[0],
            'access_token': access_token
        }

        comment_response = requests.post(comment_url, data=comment_data)

        # Check the response from adding a comment
        if comment_response.status_code == 200:
            print("Comment successfully added")  
        else:
            print("Failed to add comment", comment_response.json())
        
    else:
        print("Failed to upload photo", photo_response.json())

def multi_posting(fetch_data:list, pin=True):

    image_keys = fetch_data[0]
    caption_keys = fetch_data[1] 
    source_keys = fetch_data[2]
    title = fetch_data[-1]

    assert len(image_keys)==len(caption_keys)==len(source_keys)

    # Facebook Graph API endpoint for uploading photos
    upload_url = f"https://graph.facebook.com/v20.0/{page_id}/photos"

    # Download the photos
    
    images = [{'path': f'assets/images/Glimpses/{i}.jpg','caption': caption_keys[i] + ' | ' + source_keys[i]} for i in range(len(image_keys))]

    photo_ids = []
    for image in images:
        with open(image['path'], 'rb') as img_file:
            payload = {
                'access_token': access_token,
                'caption': image['caption'].strip(' | '),
                'published': 'false'  # 'false' to prevent auto-posting
            }
            files = {'source': img_file}

            response = requests.post(upload_url, data=payload, files=files)
            
            if response.status_code == 200:
                photo_id = response.json()['id']
                photo_ids.append(photo_id)
                print(f"Successfully uploaded {image['path']} with ID {photo_id}")
            else:
                print(f"Failed to upload {image['path']}. Error: {response.text}")

    
    if photo_ids:

        post_url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
        media_ids = [{'media_fbid': photo_id} for photo_id in photo_ids]
        
        post_payload = {
            'access_token': access_token,
            'attached_media': json.dumps(media_ids), 
            'message': title  # Main caption for the post
        }
        
        # Send the POST request to create the post
        post_response = requests.post(post_url, data=post_payload)
        
        # Check the response
        if post_response.status_code == 200:
            post_id = post_response.json()['id']
            print(f"\n\nSuccessfully created the glimpse post")
        else:
            print(f"Failed to create the glimpse post. Error: {post_response.text}")

   
    if post_id and pin:
        
        pin_url = f"https://graph.facebook.com/v20.0/{post_id}/"
        
        pin_payload = {
            'access_token': access_token,
            'is_pinned': 'true'
        }
        
        pin_response = requests.post(pin_url, data=pin_payload)
        
        if pin_response.status_code == 200:
            print(f"Successfully pinned the post!")
        else:
            print(f"Failed to pin the post. Error: {pin_response.text}")
