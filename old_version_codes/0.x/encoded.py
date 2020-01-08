import requests
from io import BytesIO
from PIL import Image


class Vcode():
    def __init__(self):
        self.verify_code_url = 'http://jwglxt.qau.edu.cn/verifycode.servlet'
        self.b_ver_code = Image.open((BytesIO(requests.get(self.verify_code_url).content)))
        self.b_ver_code.show()
        self.input_vcode = input('pleas input the verify code:')

class CP():

    def __init__(self):
        self.dog_code_url = 'http://jwglxt.qau.edu.cn/Logon.do?method=logon&flag=sess'
        self.response = requests.post(self.dog_code_url)
        self.code_response = self.response.content

        print(self.code_response)

        self.user_account = '20180203536'
        self.user_password = 'dachen33'

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

        self.login_url = 'http://jwglxt.qau.edu.cn/Logon.do?method=logon'

        self.data = {'useDogCode': '&' + self.encoded + 'RANDOMCODE=' + v_code}

        self.logon_response = requests.post(self.login_url, data=self.data)

        print(self.logon_response.status_code)

a = CP()