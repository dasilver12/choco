## Choco
A simple KakaoTalk Bot written in Python.

The bot can handle multiple rooms at a time.

- Wait! If you gonna use 'Your' Kakaotalk ID(not an extra ID), using this library to run a bot or else is not recommend. (because of critical problem with PC Kakaotalk's login, and I don't know why it happens exactly)

## Installation
1. Clone this repository
2. Move to choco directory and execute this command: `./start` (If occurs permission error execute `chmod +x start`)
3. Edit config file(config.py)
4. Open redis and run the following command:
```
redis> hset choco_auth mail [kakaotalk email]
redis> hset choco_auth password [kakaotalk password]
redis> hset choco_auth client [client name]
redis> hset choco_auth uuid [any text]
redis> hset choco_auth x_vc [x-vc token]
```
If you have base64 encoded device uuid string, enter this command:
```
redis> hset choco_auth uuid_base64 [b64 uuid text]
```
5. Run choco and authorize KakaoTalk account
6. Your account session data will be save to Redis DB (HASH: choco_session, If you want to re-authorize kakao account, remove this hash key use `HDEL` command

### Run
* On **linux/unix**: `./start`
* On **windows**: Before you run the bot, rename `start` to `run.py` and just double-click `run.py` to start the bot, as long as you have Python installed correctly. **[Use Choco on Windows Guide (Korean)](http://ssut-dev.tumblr.com/post/85705056741/windows-choco-kakaotalk-bot)**

Please check this: [Getting device\_uuid(uuid) from KakaoTalk PC](https://github.com/ssut/ChocoHelper/releases)

## Adding commands
Create new python file to `modules` directory and write your bot script like this code (full code):

```python
#-*- coding: utf-8 -*-
from modules import module
from choco.kakao.constants import ContentType
from choco.kakao.response import KakaoReponse

@module.route('Hello')
def hello(request):
    resp = 'Hi, {0}!'.format(request.session.nick)
    return KakaoResponse(resp)

@module.route('Photo', prefix=False)
def hello_photo(request):
    if message.attachment:
        return KakaoResponse('I got a photo!')
    else:
        image = os.path.join('sample', 'image.png')
        return KakaoResponse(image, content_type=ContentType.Image)

@module.route('Bye')
def leave(request):
    return KakaoResponse(None, content_type=ContentType.Leave)
```

### Request object
| key | type |
|--------|--------|
| room | KakaoRoom |
| session | KakaoSession |
| message | Message |
| attachment | dictionary (python object) |

### Message
| key | type | value |
|--------|--------|--------|
|room|int|Room(channel)'s unique identifier|
|user\_id|int|User that sent the message (not recommend that you use this)|
|user\_nick|unicode|User's nickname that sent the message (not recommend that you use this)|
|text|unicode|Message content|
|attachment|dict|Message attachment (e.g. Image, Video.., same as **request.attachment**)|
|time|datetime|Message sent time|

### KakaoRoom
| key | type| value |
|--------|--------|--------|
|id|str|Room(channel)'s unique identifier|

### KakaoSession
| key | type| value |
|--------|--------|--------|
|id|str|User that sent the message|
|nick|str|User's nickname that sent the message|
|is\_admin|bool|is admin|

### API
#### Unicode to String
```python
from choco.utils.unicode import u
a = u'가나다'
if isinstance(a, unicode):
	b = u(a)
    print type(b) # str
```

#### Get image size
```python
from choco.utils.image import get_image_size
file = '/Users/ssut/dev/choco/sample/image.png'
get_image_size(file) # ( width, height )
```

#### Get temporary filename (for send attachment)
```python
import urllib
from choco.utils.temp import generate_temp_name
link = 'http://example.com'
filename = generate_temp_name() # (absolute path) temp filename
urllib.urlretrieve(link, filename)
```

#### Generate random string
```python
from choco.utils.generator import random_str
print random_str(10) # first argument is length
print random_str(10, 'ab') # second argument is choices
```

#### Translate strings (with replace pairs dictionary)
```python
from choco.utils.text import strtr
STRTR_DICT = {
	'a': 'b',
    'c': 'd',
}
print strtr('ac', STRTR_DICT) # bd
```

## Getting help with Choco
### Install dependencies
To install dependencies, run:

```sh
pip install -r requirements.pip
```

### Support
The developer reside in [Ozinger IRC](http://ozinger.com), [Freenode IRC](http://freenode.net) and would be glad to help you. (IRC nickname is `ssut`)

If you think you have a found a bug/have a idea/suggestion, please **open a issue** here on Github.

### Requirements
Choco runs(tested) on **Python** 2.7.x. It is currently developed on **OS X** 10.9 with **Python** 2.7. (Not tested on PyPy and other envirionment)

It **requires some Python modules**. Please check **Install dependencies** section.

**Windows** users: You need to install PyCrypto manually. Please check [pykakao](https://github.com/ssut/pykakao) repository.

## License
Choco is **licensed** under the **MIT** license. The terms are as follows.

```text
The MIT License (MIT)

Copyright (c) 2014 SuHun Han

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
