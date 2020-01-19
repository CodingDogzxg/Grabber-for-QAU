import requests
from io import BytesIO
# from PIL import Image
# from threading import Thread
# import time


class Qiangke:

    def __init__(self):

        self.url = 'http://jwglxt.qau.edu.cn/jsxsd1/'

        self.log_url = 'http://jwglxt.qau.edu.cn/jsxsd1/xk/LoginToXk'

        self.session = requests.Session()

        #  请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

    def login(self, data):
        self.main_response = self.session.get(self.url, headers=self.headers)
        # print(main_response.text)
        self.after_response = self.session.post(self.log_url, headers=self.headers, data=data)
        # if self.after_response:
        #     print(self.after_response.text)

    def get_verify_code(self):
        # This is not necessarily needed
        verify_code_url = 'http://jwglxt.qau.edu.cn/verifycode.servlet'
        vercode_response = requests.get(verify_code_url, headers=self.headers)
        self.b_ver_code = BytesIO(vercode_response.content)

    def log_location(self, url):
        self.after_response = self.session.get(url)

    def session_score(self, url, data):
        res = self.session.post(url, data, headers=self.headers)
        return res