import requests
from io import BytesIO
from PIL import Image



url = 'http://jwglxt.qau.edu.cn/verifycode.servlet'

a = Image.open((BytesIO(requests.get(url).content)))
a.show()