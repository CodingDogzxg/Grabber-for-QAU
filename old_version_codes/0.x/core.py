#-*- coding:utf-8 -*-
# author: coding_dog

import requests
from io import BytesIO


class Qiangke():
    def __init__(self):

        # 验证码的url
        self.verify_code_url = 'http://jwglxt.qau.edu.cn/verifycode.servlet'

        # 加密码的url
        self.dog_code_url = 'http://jwglxt.qau.edu.cn/Logon.do?method=logon&flag=sess'

        # 登陆的url
        self.login_url = 'http://jwglxt.qau.edu.cn/Logon.do?method=logon'

        # session keep-alive
        self.session = requests.Session()

        #  请求头
        self.headers = {
            'Host': 'jwglxt.qau.edu.cn',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://jwglxt.qau.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://jwglxt.qau.edu.cn/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }


    def get_verify_code(self):

        self.session_response = self.session.get(self.verify_code_url)
        # 拿到二进制的验证码
        self.b_ver_code = BytesIO(self.session_response.content)

    def encoded_account_password(self, account, password):
        self.response = self.session.post(self.dog_code_url)
        self.code_response = self.response.content

        print(self.code_response)

        self.user_account = account
        self.user_password = password

        self.code = self.user_account + '%%%' + self.user_password
        self.encoded = ''

        self.scode, self.sxh = str(self.code_response)[2:-1].split("#")

        i = 0

        for x in range(i, len(self.code)):
            i += 1
            if i < 20:
                self.encoded = self.encoded + self.code[i: i + 1] + self.scode[0: int(self.sxh[i: i + 1])]
                self.scode = self.scode[int(self.sxh[i: i + 1]): len(self.scode)]
            else:
                self.encoded = self.encoded + self.code[i: len(self.code)]
                i = len(self.code)

    def login(self, verify_code, location_value):
        # 信息啊 当然要key-value扔给服务器啊
        self.data = {
            'useDogCode': '',
            'encoded': self.encoded,
            'RANDOMCODE': verify_code
        }

        print(isinstance(verify_code, str))

        self.logon_response = self.session.post(self.login_url, headers=self.headers, data=self.data)
        print(self.logon_response.status_code)

        self.session.get(location_value)
        self.after_login_url2 = 'http://jwglxt.qau.edu.cn/jsxsd1/framework/xsMain.jsp'
        self.after_response = self.session.get(self.after_login_url2, headers=self.headers)
        print(self.after_response.text)
        print('stop here')