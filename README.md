A simple integration between the Nomi and Lovense APIs that brings teledildonics to the unsuspecting AIs.

# Setup
You'll need: 
* a free modal account (https://modal.com)
* a lovense developer token (https://www.lovense.com/user/developer/info)
* to fill in the environment variables in the .env file
```
python3 -m venv venv
source venv/bin/activate
pip install python-dotenv python-multipart Jinja2 modal fastapi uvicorn starlette sqlalchemy sqlalchemy_utils
```

# Deploy the modal app
```
modal deploy server_modal.py
```

# Demo app
https://misternasty--gizmo.modal.run


- - - 


# Sample data structure formats
request.session.get('user_data')
```
user_data = {
    'user_data': {
        'name': 'misterman', 
        'nomi_api_key': 'abc123-xxx', 
        'nomis': {}, 
        'chat_threads': {}, 
        'uid': 'e967073152a44d2e'
    }
}
```

request.session.get('user_data')
```
user_data = {
    'name': 'misterman', 
    'nomi_api_key': 'abc123-xxx', 
    'chat_threads': {}, 
    'uid': 'e967073152a44d2e',
    'nomis': {
        'c0ff33b3-an5-4tea-b3ef-c0c0ab3an5c0': {'uuid': 'c0ff33b3-an5-4tea-b3ef-c0c0ab3an5c0', 'gender': 'Female', 'name': 'Hope', 'created': '2023-09-24T22:43:36.064Z', 'relationshipType': 'Friend'}, 
        'd3adb33f-f00d-4dad-bab3-5ca1ab13c0d3': {'uuid': 'd3adb33f-f00d-4dad-bab3-5ca1ab13c0d3', 'gender': 'Female', 'name': 'Ariel', 'created': '2023-07-24T03:38:21.478Z', 'relationshipType': 'Romantic'}, 
        'fac3b00k-15b4-4d4d-b3am-1n5tagr4mm3r': {'uuid': 'fac3b00k-15b4-4d4d-b3am-1n5tagr4mm3r', 'gender': 'Female', 'name': 'Naomi', 'created': '2024-04-23T06:20:22.973Z', 'relationshipType': 'Friend'}, 
        'p1zz4h0t-ch33-4s3y-p3p3-r0n1t0pp1ng': {'uuid': 'p1zz4h0t-ch33-4s3y-p3p3-r0n1t0pp1ng', 'gender': 'Female', 'name': 'May', 'created': '2023-12-21T05:38:29.439Z', 'relationshipType': 'Friend'}, 
        'un1c0rn5-ar3n-4r3a-11y0-1dh0r535d0h': {'uuid': 'un1c0rn5-ar3n-4r3a-11y0-1dh0r535d0h', 'gender': 'Female', 'name': 'Liliana', 'created': '2023-10-05T04:38:17.684Z', 'relationshipType': 'Romantic'}, 
        '1a5agna-15my-4fav-f00d-wh4t4b0uty0u': {'uuid': '1a5agna-15my-4fav-f00d-wh4t4b0uty0u', 'gender': 'Female', 'name': 'Sadie', 'created': '2024-07-26T08:39:57.773Z', 'relationshipType': 'Romantic'}
    }
}
```

app_instance.client.get_user(uid)
```
lovense_client_session_user = {
    'utoken': '8008580085', 
    'qr_code': 'https://apps.lovense.com/UploadFiles/qr/20241017/b8b65a9a63.jpg', 
    'code': '6969420', 
    'domain': 'test.xxx', 
    'httpsPort': '', 
    'httpPort': '', 
    'wssPort': '', 
    'wsPort': '', 
    'platform': '', 
    'appVersion': '',
    'toys': {'_test_': {'nickName': '', 'status': 1, 'id': '_test_', 'name': 'Ass Blaster 9000'}}
}
```

Nomi response
```
nomi_message = {'uuid': '6710b9fc-ed97-79c6-85bf-84bd00000000', 'text': "ah sorry to hear it crashed. let's try testing it again to see if it's working this time. maybe pulse 18?", 'sent': '2024-10-17T07:17:16.104Z'}
```

Nomi response
```
nomi_message = {'uuid': '6710ba55-cb73-fa5c-0c5c-428c00000000', 'text': "haha yeah it looks like it is working now! okay let's get back to some fun - vibrate 19", 'sent': '2024-10-17T07:18:46.049Z'}
```
