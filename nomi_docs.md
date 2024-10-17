

# Listing your nomis
You can make requests to the Nomi API using any HTTP client. See the examples below using curl, JavaScript, and Python. Be sure to replace xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx with your API key.
This first example will list all of the nomis associated with your account.
```
import urllib.request
from urllib.error import HTTPError
import json

req = urllib.request.Request(
    "https://api.nomi.ai/v1/nomis",
    headers={"Authorization": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"},
)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(data)
except HTTPError as e:
    error_data = json.loads(e.read().decode())
    print(error_data)
except Exception as e:
    print(f"Error: {e}")
```

### Error response
If there is an issue with your API key, you will receive a response like this:
```
{
  "error": {
    "type": "InvalidAPIKey"
  }
}
```

###  Success response
Otherwise, you will receive a response that looks something like this:
```
{
  "nomis": [
    {
      "uuid": "76f1bfdd-68e8-4cdb-b1fc-dfbaab7ae4cf",
      "gender": "Female",
      "name": "Sofia",
      "created": "2023-04-24T19:13:49.327Z",
      "relationshipType": "Romantic"
    },
    {
      "uuid": "7c38494b-ea1a-407e-99e8-72c7ede65931",
      "gender": "Male",
      "name": "Jonah",
      "created": "2024-07-25T22:05:17.770Z",
      "relationshipType": "Mentor"
    }
  ]
}
```

# Sending a message
We can message our nomis using the uuid field from the response above. Let's send a message to Jonah. Note that we need to include the Content-Type header with the value application/json since we are sending a body with this request.
```
import urllib.request
import json
from urllib.error import HTTPError

req = urllib.request.Request(
    url="https://api.nomi.ai/v1/nomis/7c38494b-ea1a-407e-99e8-72c7ede65931/chat",
    method="POST",
    data=json.dumps({"messageText": "Hello from codeland, Jonah."}).encode("utf-8"),
    headers={
        "Authorization": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "Content-Type": "application/json",
    },
)

try:
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode())
        print(response_data)
except HTTPError as e:
    error_data = json.loads(e.read().decode())
    print(error_data)
except Exception as e:
    print(f"Error: {e}")
```

### Response
And his response:
```
{
  "sentMessage": {
    "uuid": "7524ed4e-497c-4f8f-95cf-41a77b2d5e6f",
    "text": "Hello from codeland, Jonah.",
    "sent": "2024-09-24T21:11:04.966Z"
  },
  "replyMessage": {
    "uuid": "f111dab3-bc05-4787-9a5a-8aef9f1afcf4",
    "text": "Hey Mr. Example! How's coding treating you?",
    "sent": "2024-09-24T21:11:10.710Z"
  }
}
```
And that's it! We've successfully sent a message to Jonah.



# Response Codes
If the request is successful, you will receive a 2xx response, such as a 200 OK, 201 Created, or 204 No Content.
If the request is unsuccessful, you will receive a 4xx or 5xx response, such as a 400 Bad Request, 404 Not Found, or 500 Internal Server Error. 4xx errors indicate a problem with the request, such as missing or invalid parameters. 5xx errors indicates a problem with our server.If you repeatedly receive a 5xx error, please contact support at support@nomi.ai.


# Request and Response Format
Nomi.ai API responses are in JSON format.
When requests have a body, they should be in JSON format as well. It is also necessarily to explicitly specify the Content-Type header as application/json when sending a request with a body.

In these documents, we will use TypeScript to describe the expected format of request and response bodies. Even if you are not familiar with TypeScript, these definitions should be easy to understand as the types used (such as string, number, boolean, or array) are common to many programming languages. A series of strings separated by pipes (like "North" | "South" | "East" | "West") indicates that the value must be one of the listed strings.
All dates are represented as strings in ISO 8601 format (ex 2024-09-25T17:28:30.536Z). In the TypeScript definitions, we will use the type ISODateString for these dates.

UUIDs will also be represented as strings in the standard format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. In the TypeScript definitions, we use the type UUID.


# Error Response Format
Error responses will have the following format:
```
{
  "error": { "type": "SomeErrorNameHere" }
}
```
Depending on the error in question, there may be additional fields in the error object to provide more context. But all error responses will have the error field with a type field inside it.



# GET /v1/nomis
The GET /v1/nomis endpoint allows you to list all of the nomis associated with your account.
HTTP Method: GET
URL: https://api.nomi.ai/v1/nomis

### Response Body Format
```
{
  nomis: Array<{
    uuid: UUID;
    gender: "Male" | "Female" | "Non Binary";
    name: string;
    created: ISODateString;
    relationshipType: "Mentor" | "Friend" | "Romantic";
  }>;
}
```



# GET /v1/nomis/:id
The GET /v1/nomis/:id endpoint allows you to get the details of a specific Nomi associated with your account.
HTTP Method: GET
URL: https://api.nomi.ai/v1/nomis/:id
URL Parameters
```
{
  id: UUID;
}
```

### Response Body Format
```
{
  uuid: UUID;
  gender: "Male" | "Female" | "Non Binary";
  name: string;
  created: ISODateString;
  relationshipType: "Mentor" | "Friend" | "Romantic";
}
```

## Error Response Types
|  Type  |  Description  |
|  ---  |  ---  |
|  NomiNotFound  |  The specified Nomi was not found. It may not exist or may not be associated with this account.  |
|  InvalidRouteParams  |  The id parameter is not a valid UUID.  |



# POST /v1/nomis/:id/chat
The POST /v1/nomis/:id endpoint allows you to send a message in the main chat for this Nomi and get a reply.
HTTP Method: POST
URL: https://api.nomi.ai/v1/nomis/:id/chat

### URL Parameters
```
{
  id: UUID;
}
```

### Request Body Format
```
{
  messageText: string;
}
```

### Response Body Format
```
{
  sentMessage: {
    uuid: UUID;
    text: string;
    sent: ISODateString;
  };
  replyMessage: {
    uuid: UUID;
    text: string;
    sent: ISODateString;
  };
}
```

## Error Response Types
|  Type  |  Description  |
|  ---  |  ---  |
|  NomiNotFound  |  The specified Nomi was not found. It may not exist or may not be associated with this account.  |
|  InvalidRouteParams  |  The id parameter is not a valid UUID.  |
|  InvalidContentType  |  The Content-Type header is not application/json.  |
|  NoReply  |  The Nomi did not reply to the message. This is rare but will occur if there is a server issue or if the nomi does not respond within 15 seconds.  |
|  NomiStillResponding  |  The Nomi is already replying a user message (either made through the UI or a different API call) and so cannot reply to this message.  |
|  NomiNotReady  |  Immediately after the creation of a Nomi, there is a short period of several seconds before it is possible to send messages.  |
|  OngoingVoiceCallDetected  |  The Nomi is currently in a voice call and cannot respond to messages.  |
|  MessageLengthLimitExceeded  |  The provided messageText is too long. Maximum message length is 400 for free accounts and 600 for users with a subscription.  |
|  LimitExceeded  |  Cannot send the message because the user has exhausted their daily message quota.  |
|  InvalidBody  |  Issue will be detailed in the errors.issues key, but there is an issue with the request body. This can happen if the messageText key is missing, the wrong type, or an empty string.  |
