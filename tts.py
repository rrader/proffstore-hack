import os
import requests

def say(text, sync=False):
    # url = "http://translate.google.com/translate_tts?tl=en&q={}&total=1&idx=0&client=t&ie=UTF-8".format(text)
    # r = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}, stream=True)

    # if r.status_code == 200:
    #     with open("/tmp/say.mp3", 'wb') as f:
    #         for chunk in r:
    #             f.write(chunk)
    #     cmd = 'mpg321 /tmp/say.mp3'
    #     if not sync:
    #         cmd += ' &'
    #     os.system(cmd)
    # else:
    #     print(r.status_code)
    # cmd = 'echo "{}" | festival --tts'.format(text)
    cmd = 'espeak -ven+f3 -k5 -s150 "{}"'.format(text)
    if not sync:
        cmd += ' &'
    os.system(cmd)
