import requests

def post(fetch_data):

    page_id = ''
    access_token = ""

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