#-*- coding:utf-8 -*-
import os
import re
from io import StringIO
import requests
from PIL import Image
from xkocr import OCR


# 改编自代码喵抢课姬 知乎大佬@CodingCat
class Xuanke():

    """docstring for Xuanke"""
    def __init__(self):
        self.OCR_OBJ = OCR.Val_to_Str(os.path.split(os.path.realpath(__file__))[0] + "/dump-fuck.txt")
        self.Xuanke_Target_url = "http://"  # 目标url
        self.Xuanke_Valcode_url = "http://"  # 验证码的url
        self.Xuanke_Inquire_Course_url = "http://"  # 课程代码的url
        self.Inquire_Session = requests.session()
        self.Xuanke_Name_Cache = {}

    def check_login(self):
        try:
            NULL_F = self