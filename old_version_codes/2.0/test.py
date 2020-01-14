# import requests
#
# url = "http://codingdogzxg.github.io/grabber_vercode.html"
#
# a = requests.get(url).text.split("#")
# print(a)
#
#
# with open("ver_info.zxg", "r") as ver_file:
#     step1 = ver_file.read().split("#")
#     version = step1[1]
#     time = step1[2]
#     print(version, time)
#
# if a[1] == version and a[2] == time:
#     print("版本号 更新时间一致 无需更新")

import os
import zipfile
import shutil
# with open("temp\\2.md", "r") as a:
#     print(a.read())
#
# if not os.path.exists("temp"):
#     os.makedirs("temp")

zip1 = zipfile.ZipFile("temp\\1.zip")
zip1.extractall("temp\\")

print("1")


print("2")
os.rename("temp\\2-1.md", "temp\\2.md")
print("3")

shutil.move(r"temp\2.md", r"C:\Users\q2461\Desktop\Incremental-upgrade-master")

