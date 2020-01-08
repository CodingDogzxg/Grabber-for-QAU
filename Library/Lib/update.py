import zipfile
import requests
import os
import shutil


class Update:

    def __init__(self, dir, zip_dir, existence):

        # 获取升级的url
        self.download_url = "https://codeload.github.com/CodingDogzxg/Grabber/zip/update"
        self.ver_url = "http://codingdogzxg.github.io/grabber_vercode.html"

        self.dir = dir

        self.zip_dir = zip_dir

        # 是否需要更新
        self.update_bore = False

        # 是否存在文件
        self.version_file = existence

        # 是否完成操作
        self.done = False


    def check_update(self):

        # 提取当前版本信息
        # try:
        with open(self.dir, "r") as ver_file:
            info_all = ver_file.read().split("#")
            version_info = info_all[1]
            update_time = info_all[2]
            print("1")

            # 检测是否与服务器版本信息一致
            self.r_t = requests.get(self.ver_url).text
            code_lastest = self.r_t.split("#")
            if code_lastest[1] == version_info and code_lastest[2] == update_time:
                self.update_bore = False
            elif code_lastest[1] != version_info or code_lastest[2] != update_time:
                self.update_bore = True
                self.update_judgement()

        # except FileNotFoundError:
        #     self.version_file = False
        #     print("2")

    def update_judgement(self):

        # if self.update_bore:

        # 拿到二进制的响应文件
        r = requests.get(self.download_url)

        # 检测目录是否存在 不存在创建目录
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # 写文件 把二进制的响应文件保存
        with open(r"temp\Grabber-update.zip", "wb") as file_new:
            file_new.write(r.content)

        # 把保存的文件解压缩
        update_zip = zipfile.ZipFile(r"temp\Grabber-update.zip")

        # try:
        #     dir = ""
        #     a = os.path.abspath("ver_info.zxg")
        #     dir2 = a.split("\\")
        #     for x in dir2:
        #         if x != "ver_info.zxg" and x != "Grabber-master":
        #             dir = dir + x + "\\"

        update_zip.extractall("temp\\")

        self.done = True

        # ---------------------------------------------------------------------------
        # 很明显递归和shutil copy的权限相悖 并不是我懒 也不是我我不会 而是真的没法写 19／8／22
        # 归根到底还是我懒得写了 毕竟不能cover所有人的情况
        # def move_file(b_dir, t_dir):
        #     for filename in os.listdir(b_dir):
        #         abs_file = os.path.join(os.getcwd(), b_dir, filename)
        #         if os.path.isdir(abs_file):
        #             b1_dir = os.path.join(b_dir, filename)
        #             t1_dir = os.path.join(t_dir, filename)
        #             move_file(b1_dir, t1_dir)
        #         else:
        #             shutil.copy(b_dir, t_dir)


        # -------------------------------------------------------------------
        # os.rename("temp\\Grabber-update", "temp\\Grabber")
        #
        # shutil.move("temp\\Grabber", r"{}".format(self.zip_dir))
        #
        # c_zip = zipfile.ZipFile("temp\\Grabber.zip", "w")
        # print(os.path.exists("temp\\Grabber"))
        #
        #
        # a_dir = "temp\\Grabber"
        #
        # def move_files(abs_dir, zip_file):
        #     for file_name in os.listdir(abs_dir):
        #         abs_file = os.path.join(os.getcwd(), abs_dir, file_name)
        #         if os.path.isdir(abs_file):
        #             rel_file = abs_file[len(os.getcwd()) + 1:]
        #             zip_file.write(rel_file)
        #             move_files(abs_file, zip_file)
        #         else:
        #             rel_file = abs_file[len(os.getcwd()) + 1:]
        #             zip_file.write(rel_file)
        #     zip_file.close()
        #
        # move_files(a_dir, c_zip)
        # ------------------------------------------------------------------

        # c_zip.write("{}".format(self.zip_dir + r"\Grabber\temp\Grabber"))
        # c_zip.close()

        # print(self.zip_dir)
        # c_zip.extractall("{}".format(self.zip_dir))



        # except FileNotFoundError:
        #     pass
