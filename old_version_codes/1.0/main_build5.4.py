import requests
from io import BytesIO
from PIL import Image
from threading import Thread
import time


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

        self.session_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'jwglxt.qau.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        }

    # 这是关于重定向问题解决的测试方法 问题依然没有解决 4/24
    # 这几行代码可有可无 问题无法解决 5/4
    def prepare_process(self):
        self.pre_url1 = 'http://jwglxt.qau.edu.cn/'
        self.pre_url2 = 'http://jwglxt.qau.edu.cn/js/jspublic.js'
        self.pre_url3 = 'http://jwglxt.qau.edu.cn/js/prototype.js'
        self.session.get(self.pre_url1)
        self.session.get(self.pre_url2)
        self.session.get(self.pre_url3)

    # 把验证码画在屏幕上
    def draw_verify_code(self):

        # 拿到验证码的url的response
        self.session_response = self.session.get(self.verify_code_url)

        # 拿到的response里有content就是验证码 把二进制的验证码扔进你的内存里 然后再用PIL打开这个二进制内存文件 在show()之前不会显示出来
        self.b_ver_code = Image.open((BytesIO(self.session_response.content)))

        # 多线程防卡死 target是目标函数 args是transfer到target函数里的变量
        self.t1 = Thread(target=self.display_verify_code, args=(self.b_ver_code,))
        self.t1.start()
        self.verify_code = input('please input the verify code:')

        # 把cookies从请求头里提取出来
        self.cookie_t = self.session_response.headers['Set-Cookie'].split(';')[0].split("=")[1]
        print(self.cookie_t)

        self.cookies = {
            'JSESSIONID': self.cookie_trans
        }

        self.session_get_response = self.session.get('http://jwglxt.qau.edu.cn/', headers=self.session_headers, cookies=self.cookies)

    # 这是配合多线程 target的函数 image就是多线程里写的args
    def display_verify_code(self, image):
        image.show()

    # 把你的账号密码加密的神奇代码 从网站的js分析以后抄来的
    def encoded_account_password(self):
        self.response = self.session.post(self.dog_code_url)
        self.code_response = self.response.content

        print(self.code_response)

        self.user_account = input('your account:')
        self.user_password = input('your password:')

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

        print(self.encoded)

    # 实现登陆的函数
    def login(self):

        # 信息啊 当然要key-value扔给服务器啊
        self.data = {
            'useDogCode': '',
            'encoded': self.encoded,
            'RANDOMCODE': self.verify_code
        }

        print(isinstance(self.verify_code,str))

        self.logon_response = self.session.post(self.login_url, headers=self.headers, data=self.data)
        print(self.logon_response.status_code)

        #print(self.logon_response2.status_code, self.logon_response.history)

        #self.redirection_url = self.logon_response.headers['location']

        # 涉及302重定向问题 requests可以跟踪重定向，我正在百科.... 目前无法解决这个问题，只能手动复制Location
        #self.after_login_url1 = 'http://jwglxt.qau.edu.cn/jsxsd1/xk/LoginToXk?method=jwxt&ticket= ??? ' #这里的???是Location 自己复制一个加进来
        #self.session.get(self.after_login_url1)

        #self.after_login_url2 = 'http://jwglxt.qau.edu.cn/jsxsd1/framework/xsMain.jsp'
        #self.after_response = self.session.get(self.after_login_url2, headers=self.headers)
        #print(self.after_response.text)



