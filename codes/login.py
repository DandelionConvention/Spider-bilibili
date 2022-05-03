from MyQR import myqr
import requests
import json
import time
from PIL import Image
import os
import re

url1 = 'http://passport.bilibili.com/qrcode/getLoginUrl'
url2 = 'http://passport.bilibili.com/qrcode/getLoginInfo'
url3 = 'https://api.bilibili.com/x/web-interface/nav'

# f-string: formatted string literals, 格式化字符串常量。
# 功能同str.format() %-formatting,
# 较两者更简洁易用，推荐使用
# 需要注意的是，Python3.6及以后的版本可用。

def login_code():
    url_json = requests.get(url1).json()
    qr_url = url_json['data']['url']
    key = url_json['data']['oauthKey']

    myqr.run(words=qr_url, colorized=True, save_name=f"{key}.jpg")

    img_1 = Image.open(f"{key}.jpg")
    img_1.show()

    data1 = {"oauthKey": key}

    times_out = 60
    times_ = 0
    try:
        while True:
            time.sleep(1)
            times_ += 1
            r1 = requests.post(url2, data=data1).json()
            if r1['status']:
                print("login")
                os.remove(f"{key}.jpg")
                break
            if times_ >= times_out:
                return "扫码超时重新启动，程序关闭"

        text1 = r1['data']['url'].replace('https://passport.biligame.com/crossDomain?', '')
        text2 = re.split("&", text1)

        cookie = {}
        for text3 in text2:
            text4 = re.split("=", text3)
            if text4[0] == "gourl":
                continue
            cookie[text4[0]] = text4[1]

        user_json = requests.get(url3, cookies=cookie).json()
        uid = user_json['data']['mid']
        uname = user_json['data']['uname']

        with open(f"{uid}_{uname}_cookie.json", "w", encoding='utf-8') as f:
            json.dump(cookie, f)
        f.close()

        os.remove(f"{key}.jpg")

        return {'state':True, 'data':cookie}

    except:
        return {'state':False, 'data':r1['data']}

