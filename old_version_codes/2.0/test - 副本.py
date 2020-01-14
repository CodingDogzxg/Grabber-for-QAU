# import zipfile
#
# a = zipfile.ZipFile("2.zip")
#
# for name in a.namelist():
#     if not name == "1/":
#         print(name)
#         a.extract(name)


import shutil
import os

def move_file(b_dir, t_dir):
    for filename in os.listdir(b_dir):
        print(filename)
        abs_file = os.path.join(os.getcwd(), b_dir, filename)
        print(abs_file)
        if os.path.isdir(abs_file):
            b1_dir = os.path.join(b_dir, filename)
            t1_dir = os.path.join(t_dir, filename)
            move_file(b1_dir, t1_dir)
        else:
            shutil.copy(b_dir, t_dir)

move_file(r"C:\Users\q2461\Desktop\Incremental-upgrade-master\temp", "2\\")