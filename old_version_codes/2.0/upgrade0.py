import zipfile
import requests
import os


class Update:

    def __init__(self, code):

        # 获取升级的url
        self.download_url = "https://codeload.github.com/CodingDogzxg/Incremental-upgrade/zip/master"
        self.ver_url = "http://codingdogzxg.github.io/grabber_vercode.html"

        self.code = code
        self.update_bore = False

        self.check_update()
        self.update_judgement()

    def check_update(self):

        try:
            with open("ver_info.zxg", "r") as ver_file:
                info_all = ver_file.read().split("#")
                version_info = info_all[1]
                update_time = info_all[2]
        except FileNotFoundError:
            print("未找到版本号文件 请手动更新")

        code_lastest = requests.get(self.ver_url).text.split("#")
        if code_lastest[1] == version_info and code_lastest[2] == update_time:
            print("版本号 更新时间一致 无需更新")
        elif code_lastest[1] != version_info or code_lastest[2] != update_time:
            self.update_bore = True

    def update_judgement(self):

        if self.update_bore:

            # 拿到二进制的响应文件
            r = requests.get(self.download_url)

            # 写文件 把二进制的响应文件保存
            with open("Incremental-upgrade.zip", "wb") as file_new:
                file_new.write(r.content)

            # 把保存的文件解压缩
            update_zip = zipfile.ZipFile("Incremental-upgrade.zip")

            try:
                dir = ""
                a = os.path.abspath("ver_info.zxg")
                dir2 = a.split("\\")
                for x in dir2:
                    if x != "ver_info.zxg" and x != "Incremental-upgrade-master":
                        dir = dir + x + "\\"
                        print(dir)

                update_zip.extractall(path=dir)

            except FileNotFoundError:
                print("获取文件路径失败")

a = Update('1')