import requests
from io import BytesIO
from PIL import Image
from threading import Thread


class Qiangke():

    def __init__(self):

        # the url of verify code
        self.verify_code_url = 'http://jwglxt.qau.edu.cn/verifycode.servlet'

        # build an example of session to keep connection alive
        self.session = requests.Session()

    def draw_verify_code(self):    # a function that can draw the verify code on the screen

        self.b_ver_code = Image.open((BytesIO(self.session.get(self.verify_code_url).content)))
        t1 = Thread(target=self.display, args=(self.b_ver_code,))
        t1.start()
        self.verify_code = input('pleas input the verify code:')

    def display(self,image):
        image.show()

a = Qiangke()
a.draw_verify_code()