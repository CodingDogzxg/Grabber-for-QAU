import requests
import re
import time


class Update:
    def __init__(self):

        self.version_info_url = 'https://github.com/CodingDogzxg/Grabber-for-QAU/blob/ver_info/ver_info.zxg'
        self.gotten_response = False

        self.re_found = False
        self.re_time_usage = 0

        self.cloud_info_dict = {'version': '', 'time': ''}

        self.network_re()

    def network_re(self):
        re_reponse = requests.get(self.version_info_url)
        if re_reponse.status_code == 200:
            self.gotten_response = True
            try:
                time1 = time.time()
                response_content = str(re_reponse.content)[1:-1]
                re_findall = re.search('#Version#.*#Version#', response_content)
                cloud_info = re_findall.group()[9:-9].split("#")
                self.cloud_info_dict['version'] = cloud_info[0]
                self.cloud_info_dict['time'] = cloud_info[1]
                time2 = time.time()
                self.re_time_usage = time2 - time1
                self.re_found = True
            except AttributeError:
                self.re_found = False
