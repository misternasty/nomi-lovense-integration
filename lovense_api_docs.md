

### Step 1: Configure the developer dashboard
### Step 2: Find your user's toy(s)

1. Get your developer token from the Lovense developer dashboard.
2. Your server calls Lovense server's API (use POST request)
```
const result = await axios.post(
    "https:api.lovense-api.com/api/lan/getQrCode",
    {
      token: "your developer token", Lovense developer token
      uid: "11111", user ID on your website
      uname: "user name", user nickname on your website
      utoken: md5(uid + "salt"), This is for your own verification purposes. We suggest you to generate a unique token/secret for each user. This allows you to verify the user and avoid others faking the calls.
      v: 2,
    }
  )
```

### Response
```
{
  code: 0
  message: "Success"
  result: true
  data: {
    "qr": "https:test2.lovense.com/UploadFiles/qr/20220106/xxx.jpg", QR code picture
    "code": "xxxxxx"
  }
}
```
  
3. Once the user scans the QR code with the Lovense Remote app, the app will invoke the Callback URL you've provided in the developer dashboard. The Lovense server is no longer required. All communications will go from the app to your server directly.
Tip: The QR code will expire after 4 hours.
The Lovense Remote app will send the following POST to your server:
```
{
  "uid": "xxx",
  "appVersion": "4.0.3",
  "toys": {
    "xxxx": {
      "nickName": "",
      "name": "max",
      "id": "xxxx",
      "status": 1
    }
  },
  "wssPort": "34568",
  "httpPort": "34567",
  "wsPort": "34567",
  "appType": "remote",
  "domain": "192-168-1-44.lovense.club",
  "utoken": "xxxxxx",
  "httpsPort": "34568",
  "version": "101",
  "platform": "android"
}
```


### Step 3: Command the toy(s)
3A: By local application
3B: By server
Depending on whether the user's device is in the same LAN environment, you can use the following methods to command the toy(s). With the same command line, different parameters will lead to different results.


### Step 3A: By local application
If the user's device is in the same LAN environment, a POST request to Lovense Remote can trigger a toy response. In this case, your server and Lovense's server are not required.
If the user uses the mobile version of Lovense Remote app, the domain and httpsPort are accessed from the callback information. If the user uses Lovense Remote for PC, the domain is 127-0-0-1.lovense.club, and the httpsPort is 30010

## GetToys Request
Get the user's toy(s) information.

API URL: https:{domain}:{httpsPort}/command
Request Protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON
 
Headers:
|  Name  |  Description  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |
|  X-platform  |  The name of your application  |  Will be displayed on the Lovense Remote screen.  |  yes  |
 
GetToys Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |

GetToys Request example:
```
{
  "command": "GetToys"
}
```

### GetToys Response example:
```
{
  "code": 200,
  "data": {
    "toys": "{  \"f082c00246fa\" : {    \"id\" : \"f082c00246fa\",    \"status\" : \"1\",    \"version\" : \"\",    \"name\" : \"nora\",    \"battery\" : 60,    \"nickName\" : \"\",    \"shortFunctionNames\" : [      \"v\",    \"r\"    ],    \"fullFunctionNames\" : [       \"Vibrate\",    \"Rotate\"    ]  }}",
  "platform": "ios",
  "appType": "remote"
  },
  "type": "OK"
}
```

### GetToyName Request
Get the user's toy(s) name.
 
API URL: https:{domain}:{httpsPort}/command
Request Protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Headers:
|  Name  |  Description  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |
|  X-platform  |  The name of your application  |  Will be displayed on the Lovense Remote screen.  |  yes  |

GetToyName Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |

GetToyName Request example:
```
{
  "command": "GetToyName"
}
```

GetToyName Response example:
```
{
  "code": 200,
  "data": ["Domi", "Nora"],
  "type": "OK"
}
```


## Function Request
API URL: https:{domain}:{httpsPort}/command
Request Protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Headers:
|  Name  |  Description  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |
|  X-platform  |  The name of your application  |  Will be displayed on the Lovense Remote screen.  |  yes  |

Function Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  action  |  Control the function and strength of the toy  |  string  |  Actions can be: Vibrate, Rotate, Pump, Thrusting, Fingering, Suction, Depth, Stroke, or Stop. Use All to make all functions respond. Use Stop to stop the toy’s response.  |  yes  |
|  timeSec  |  Total running time  |  double  |  0 = indefinite length; Otherwise, running time should be greater than 1.  |  yes  |
|  loopRunningSec  |  Running time  |  double  |  Should be greater than 1  |  no  |
|  loopPauseSec  |  Suspend time  |  double  |  Should be greater than 1  |  no  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will be applied to all toys  |  no  |
|  stopPrevious  |  Stop all previous commands and execute current commands  |  int  |  Default: 1; If set to 0 , it will not stop the previous command.  |  no  |
|  apiVer  |  The version of the request  |  int  |  Always use 1  |  yes  |

action Ranges:
* Vibrate:0 ~ 20
* Rotate: 0~20
* Pump:0~3
* Thrusting:0~20
* Fingering:0~20
* Suction:0~20
* Depth: 0~3
* Stroke: 0~100*
* All:0~20
**Stroke should be used in conjunction with Thrusting, and there should be a minimum difference of 20 between the minimum and maximum values. Otherwise, it will be ignored.**

### Function Request example 1:
Vibrate toy ff922f7fd345 at 16th strength, run 9 seconds, then suspend 4 seconds. It will be looped. Total running time is 20 seconds.
```
{
  "command": "Function",
  "action": "Vibrate:16",
  "timeSec": 20,
  "loopRunningSec": 9,
  "loopPauseSec": 4,
  "toy": "ff922f7fd345",
  "apiVer": 1
}
```

### Function Request example 2:
Vibrate 9 seconds at 2nd strength
Rotate toys 9 seconds at 3rd strength
Pump all toys 9 seconds at 4th strength
For all toys, it will run 9 seconds then suspend 4 seconds. It will be looped. Total running time is 20 seconds.
```
{
  "command": "Function",
  "action": "Vibrate:2,Rotate:3,Pump:3",
  "timeSec": 20,
  "loopRunningSec": 9,
  "loopPauseSec": 4,
  "apiVer": 1
}
```

### Function Request example 3:
Vibrate 9 seconds at 2nd strength
The rest of the functions respond to 10th strength 9 seconds
```
{
  "command": "Function",
  "action": "Vibrate:2,All:10",
  "timeSec": 20,
  "loopRunningSec": 9,
  "loopPauseSec": 4,
  "apiVer": 1
}
```

### Function Request example 4:
Thrust 20 seconds at 10th strength and stroke range of 0-20
```
{
  "command": "Function",
  "action": "Stroke:0-20,Thrusting:10",
  "timeSec": 20,
  "apiVer": 1
}
```

### Function Request example 5:
Stop all toys
```
{
  "command": "Function",
  "action": "Stop",
  "timeSec": 0,
  "apiVer": 1
}
```


# Pattern Request
If you want to change the way the toy responds very frequently you can use a pattern request. To avoid network pressure and obtain a stable response, use the commands below to send your predefined patterns at once.

API URL: https:{domain}:{httpsPort}/command
Request protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Headers:
|  Name  |  Description  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |
|  X-platform  |  The name of your application  |  Will be displayed on the Lovense Remote screen.  |  yes  |

Pattern Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  rule  |  "V:1;F:v,r,p,t,f,s,d;S:1000#"  |  string  |  The strength of r and p, d will automatically correspond to v.  |  yes  |
|  strength  |  The pattern. For example: 20;20;5;20;10  |  string  |  No more than 50 parameters. Use semicolon ; to separate every strength.  |  yes  |
|  timeSec  |  Total running time  |  double  |  0 = indefinite length; Otherwise, running time should be greater than 1.  |  yes  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will apply to all toys  |  no  |
|  apiVer  |  The version of the request  |  int  |  Always use 2  |  yes  |

### rule string format: 
**"V:1;F:v,r,p,t,f,s,d;S:1000#"**
* V:1; Protocol version, this is static.;
* F:v,r,p,t,f,s,d; Features: v is vibrate, r is rotate, p is pump, t is thrusting, f is fingering, s is suction, d is depth, this should match the strength below.;
* F:; Leave blank to make all functions respond.;
* S:1000; Intervals in Milliseconds, should be greater than 100.
  
### Pattern Request example 1:
Vibrate the toy as defined. The interval between changes is 1 second. Total running time is 9 seconds.
```
{
  "command": "Pattern",
  "rule": "V:1;F:v;S:1000#",
  "strength": "20;20;5;20;10",
  "timeSec": 9,
  "toy": "ff922f7fd345",
  "apiVer": 2
}
```

### Pattern Request example 2:
Vibrate the toys as defined. The interval between changes is 0.1 second. Total running time is 9 seconds.
If the toys include Nora or Max, they will automatically rotate or pump, you don't need to define it.
```
{
  "command": "Pattern",
  "rule": "V:1;F:v,r,p;S:100#",
  "strength": "20;20;5;20;10",
  "timeSec": 9,
  "apiVer": 2
}
 ```


# PatternV2 Request
The 2nd version of the Pattern Request includes four operations: Setup, Play, Stop, and SyncTime. For now, it is only available for the position control of Solace Pro. It is suitable for scenarios with a predefined pattern.

API URL: https:{domain}:{httpsPort}/command
Request protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Headers:
|  Name  |  Description  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |
|  X-platform  |  The name of your application  |  Will be displayed on the Lovense Remote screen.  |  yes  |

PatternV2 Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  type  |  Type of operation  |  string  |  /  |  yes  |
|  actions  |  [{"ts":0,"pos":10},{"ts":100,"pos":100},{"ts":200,"pos":10},{"ts":400,"pos":15},{"ts":800,"pos":88}]  |  array of object  |  Each action consists of a timestamp (in ms) and a corresponding position value (0~100); - ts: Must be greater than the previous one and the maximum value is 7200000. Invalid data will be removed; - pos: The value range is 0~100. Invalid data will be removed.  |  yes  |
|  apiVer  |  The version of the request  |  int  |  Always use 1  |  yes  |


### PatternV2 Request example:
```
{
  "command": "PatternV2",
  "type": "Setup",
  "actions": [
    { "ts": 0, "pos": 10 },
    { "ts": 100, "pos": 100 },
    { "ts": 200, "pos": 10 },
    { "ts": 400, "pos": 15 },
    { "ts": 800, "pos": 88 }
  ],
  "apiVer": 1
}
```

### PatternV2 Response example:
```
{
  "code": 200,
  "type": "ok"
}
```


# Play
Play the predefined pattern.

API URL: https:{domain}:{httpsPort}/command
Request protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Play Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  startTime  | The start time of playback  |  int  |  The value range is 0~7200000 (in ms). If you don’t include this, it will start playing from 0.  |  yes  |
| offsetTime  |  The client-server offset time  |  int  |  The value range is 0~15000 (in ms). If you don’t include this, it will be set to 0.  |  yes  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will be applied to all connected toys.  |  yes  |
|  apiVer  |  The version of the request  |  int  |  Always use 1  |  yes  |

Play Request example:
```
{
  "command": "PatternV2",
  "type": "Play",
  "toy": "ff922f7fd345",
  "startTime": 100,
  "offsetTime": 300,
  "apiVer": 1
}
```

Play Response example:
```
{
  "code": 200,
  "type": "ok"
}
```


# Stop
Stop playing the predefined pattern.

API URL: https:{domain}:{httpsPort}/command
Request protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Stop Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will be applied to all connected toys.  |  yes  |
|  apiVer  |  The version of the request  |  int  |  Always use 1  |  yes  |

Stop Request example:
{
    "command": "PatternV2",
    "type": "Stop",
    "toy": "ff922f7fd345",
    "apiVer": 1
  }
  
### Stop Response example:
```
{
  "code": 200,
  "type": "ok"
}
```


# Preset Request
API URL: https:{domain}:{httpsPort}/command
Request protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Headers:
|  Name  |  Description  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |
|  X-platform  |  The name of your application  |  Will be displayed on the Lovense Remote screen.  |  yes  |

Preset Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  name  |  Preset pattern name  |  string  |  We provide four preset patterns in the Lovense Remote app: pulse, wave, fireworks, earthquake  |  yes  |
|  timeSec  |  Total running time  |  double  |  0 = indefinite length  |  yes  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will be applied to all toys  |  no  |
|  apiVer  |  The version of the request  |  int  |  Always use 1  |  yes  |


### Preset Request example:
Vibrate the toy with pulse pattern, the running time is 9 seconds.
```
{
  "command": "Preset",
  "name": "pulse",
  "timeSec": 9,
  "toy": "ff922f7fd345",
  "apiVer": 1
}
```

### Preset Response example:
```
{
  "code": 200,
  "type": "ok"
}
```

### Preset Error codes:
|  Code  |  Message  |
|  500  |  HTTP server not started or disabled  |
|  400  |  Invalid Command  |
|  401  |  Toy Not Found  |
|  402  |  Toy Not Connected  |
|  403  |  Toy Doesn't Support This Command  |
|  404  |  Invalid Parameter  |
|  506  |  Server Error. Restart Lovense Connect.  |



# Step 3B: By server
If your application can’t establish a LAN connection to the user’s Lovense Remote app, you can use the Server API to connect the user’s toy.

## Function Request
API URL: https:api.lovense-api.com/api/lan/v2/command
Request Protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Request Format: JSON

Function Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  token  |  Your developer token  |  string  |  /  |  yes  |
|  uid  |  Your user’s ID  |  string  |  To send commands to multiple users at the same time, add all the user IDs separated by commas. The toy parameter below will be ignored and the commands will go to all user toys by default.  |  yes  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  action  |  Control the function and strength of the toy  |  string  |  Actions can be Vibrate, Rotate, Pump, Thrusting, Fingering, Suction, or Stop. Use Stop to stop the toy’s response.  |  yes  |
|  timeSec  |  Total running time  |  double  |  0 = indefinite length; Otherwise, running time should be greater than 1.  |  yes  |
| loopRunningSec | Running time  |  double  |  Should be greater than 1.  |  no  |
| loopPauseSec  |  Suspend time  |  double  |  Should be greater than 1.  |  no  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will be applied to all toys  |  no  |
|  stopPrevious  |  Stop all previous commands and execute current commands  |  int  |  Default: 1, If set to 0 , it will not stop the previous command.  |  no  |
|  apiVer  |  The version of the request  |  int  |  Always use 1  |  yes  |

**action Range:**
* Vibrate:0 ~ 20
* Rotate: 0~20
* Pump:0~3
* Thrusting:0~20
* Fingering:0~20
* Suction:0~20	yes


### Function Request example 1:
Vibrate toy ff922f7fd345 at 16th strength, run 9 seconds then suspend 4 seconds. It will be looped. Total running time is 20 seconds.
```
{
  "token": "FE1TxWpTciAl4E2QfYEfPLvo2jf8V6WJWkLJtzLqv/nB2AMos9XuWzgQNrbXSi6n",
  "uid": "1132fsdfsd",
  "command": "Function",
  "action": "Vibrate:16",
  "timeSec": 20,
  "loopRunningSec": 9,
  "loopPauseSec": 4,
  "apiVer": 1
}
```

### Function Request example 2:
Vibrate 9 seconds at 2nd strength
Rotate toys 9 seconds at 3rd strength
Pump all toys 9 seconds at 4th strength
For all toys, it will run 9 seconds then suspend 4 seconds. It will be looped. Total running time is 20 seconds.
```
{
  "token": "FE1TxWpTciAl4E2QfYEfPLvo2jf8V6WJWkLJtzLqv/nB2AMos9XuWzgQNrbXSi6n",
  "uid": "1132fsdfsd",
  "command": "Function",
  "action": "Vibrate:2,Rotate:3,Pump:3",
  "timeSec": 20,
  "loopRunningSec": 9,
  "loopPauseSec": 4,
  "apiVer": 1
}
```


## Pattern Request
If you want to change the way the toy responds very frequently you can use a pattern request. To avoid network pressure and obtain a stable response, use the commands below to send your predefined patterns at once.

API URL: https:api.lovense-api.com/api/lan/v2/command
Request protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Response Format: JSON

Pattern Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  token  |  Your developer token  |  string  |  /  |  yes  |
|  uid  |  Your user’s ID  |  string  |  To send commands to multiple users at the same time, add all the user IDs separated by commas. The toy parameter below will be ignored and the commands will go to all user toys by default.  |  yes  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  rule  |  "V:1;F:v,r,p,t,f,s;S:1000#"  |  string  |  The strength of r and p will automatically correspond to v.  |  yes  |
|  strength  |  The pattern. For example: 20;20;5;20;10  |  string  |  No more than 50 parameters. Use semicolon ; to separate every strength.  |  yes  |
|  timeSec  |  Total running time  |  double  |  0 = indefinite length; Otherwise, running time should be greater than 1.  |  yes  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will apply to all toys  |  no  |
|  apiVer  |  The version of the request  |  int  |  Always use 2  |  yes  |

### rule string format:
**"V:1;F:v,r,p,t,f,s;S:1000#"**
* V:1; Protocol version, this is static;
* F:v,r,p,t,f,s; Features: v is vibrate, r is rotate, p is pump, t is thrusting, f is fingering, s is suction, this should match the strength below;
* S:1000; Intervals in Milliseconds, should be greater than 100.


### Pattern Request example 1:
Vibrate the toy as defined. The interval between changes is 1 second. Total running time is 9 seconds.
```
{
  "token": "FE1TxWpTciAl4E2QfYEfPLvo2jf8V6WJWkLJtzLqv/nB2AMos9XuWzgQNrbXSi6n",
  "uid": "1ads22adsf",
  "command": "Pattern",
  "rule": "V:1;F:v;S:1000#",
  "strength": "20;20;5;20;10",
  "timeSec": 9,
  "apiVer": 2
}
```

### Pattern Request example 2:
Vibrate the toys as defined. The interval between changes is 0.1 second. Total running time is 9 seconds.
If the toys include Nora or Max, they will automatically rotate or pump, you don't need to define it.
```
{
  "token": "FE1TxWpTciAl4E2QfYEfPLvo2jf8V6WJWkLJtzLqv/nB2AMos9XuWzgQNrbXSi6n",
  "uid": "1ads22adsf",
  "command": "Pattern",
  "rule": "V:1;F:v,r,p;S:100#",
  "strength": "20;20;5;20;10",
  "timeSec": 9,
  "apiVer": 2
}
```


## Preset Request
API URL: https:api.lovense-api.com/api/lan/v2/command
Request protocol: HTTPS Request
Method: POST
Request Content Type: application/json
Request Format: JSON

Preset Parameters:
|  Name  |  Description  |  Type  |  Note  |  Required  |
|  ---  |  ---  |  ---  |  ---  |  ---  |
|  token  |  Your developer token  |  string  |  /  |  yes  |
|  uid  |  Your user’s ID  |  string  |  To send commands to multiple users at the same time, add all the user IDs separated by commas. The toy parameter below will be ignored and the commands will go to all user toys by default.  |  yes  |
|  command  |  Type of request  |  string  |  /  |  yes  |
|  name  |  Preset pattern name  |  string  |  We provide four preset patterns in the Lovense Remote app: pulse, wave, fireworks, earthquake  |  yes  |
|  timeSec  |  Total running time  |  double  |  0 = indefinite length  |  yes  |
|  toy  |  Toy ID  |  string  |  If you don’t include this, it will be applied to all toys  |  no  |
|  apiVer  |  The version of the request  |  int  |  Always use 1  |  yes  |


### Preset Request example:
Vibrate the toy with pulse pattern, the running time is 9 seconds.
```
{
  "token": "FE1TxWpTciAl4E2QfYEfPLvo2jf8V6WJWkLJtzLqv/nB2AMos9XuWzgQNrbXSi6n",
  "uid": "1adsf2323",
  "command": "Preset",
  "name": "pulse",
  "timeSec": 9,
  "apiVer": 1
}
```

### Preset Response example:
```
{
  "result": true,
  "code": 200,
  "message": "Success"
}
```

### Preset Server error codes:
|  Code  |  Message  |
|  ---  |  ---  |
|  200  |  Success  |
|  400  |  Invalid command  |
|  404  |  Invalid Parameter  |
|  501  |  Invalid token  |
|  502  |  You do not have permission to use this API  |
|  503  |  Invalid User ID  |
|  507  |  Lovense APP is offline  |


  
  