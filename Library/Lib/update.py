import requests
from lxml import etree


class Update:
    def __init__(self):

        self.version_info_url = 'https://github.com/CodingDogzxg/Grabber-for-QAU/blob/master/ver_info.zxg'
        self.gotten_response = False

        self.xpath_match = False

        self.cloud_info_dict = {'version': '', 'time': ''}

        self.network_re()

    def network_re(self):
        re_reponse = requests.get(self.version_info_url)
        if re_reponse.status_code == 200:
            self.gotten_response = True
            try:
                response_content = str(re_reponse.content)
                cloud_match_xml = etree.HTML(response_content)
                cloud_match = cloud_match_xml.xpath('string(// *[ @ id = "LC1"])')
                cloud_info = cloud_match[9:-9].split("#")
                self.cloud_info_dict['version'] = cloud_info[0]
                self.cloud_info_dict['time'] = cloud_info[1]
                self.xpath_match = True
            except AttributeError:
                self.xpath_match = False


            # try:
            #     response_content = str(re_reponse.content)[1:-1]
            #     re_findall = re.search('#Version#.*#Version#', response_content)
            #     cloud_info = re_findall.group()[9:-9].split("#")
            #     self.cloud_info_dict['version'] = cloud_info[0]
            #     self.cloud_info_dict['time'] = cloud_info[1]
            #     self.re_found = True
            # except AttributeError:
            #     self.re_found = False
