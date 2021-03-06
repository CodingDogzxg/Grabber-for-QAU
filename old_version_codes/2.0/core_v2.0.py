#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: coding_dog

from tkinter import *
from tkinter import messagebox
from threading import Thread
from os import system
from webbrowser import open_new
from qkcore import Qiangke
# from checkn import CheckNecessary
import tkinter
import PIL.Image, PIL.ImageTk
import pyperclip
import json
import requests


class ModifyWindow(Frame):

    # 此类仅完成界面的绘制 具体时间执行代码在QK类以及重构模块core的Qiangke类里
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Grabber for QAU By CodingDog_zxg Ver2.0')
        self.master.geometry('640x480')
        self.createWidgets()
        self.log_successfully = False


    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.Locationval = Label(self.top, text='Location: ')
        self.Locationval.place(relx=0, rely=0, relwidth=0.089, relheight=0.053)

        self.Instruction = Button(self.top, text='理论效果', fg='#0000CD', underline=0, command=self.gif_class)
        self.Instruction.place(relx=0.211, rely=0, relwidth=0.089, relheight=0.053)

        self.Instruction = Button(self.top, text='使用帮助', fg='#0000CD', underline=0, command=self.ins_open_txt)
        self.Instruction.place(relx=0.3, rely=0, relwidth=0.089, relheight=0.053)

        self.LocationvalVar = StringVar(value='')
        self.Location = Entry(self.top, textvariable=self.LocationvalVar)
        self.Location.place(relx=0, rely=0.053, relwidth=0.389, relheight=0.053)

        self.Paste = Button(self.top, text='粘贴剪切板', command=self.paste_info)
        self.Paste.place(relx=0.0436, rely=0.138, relwidth=0.129, relheight=0.09)

        self.EnterLct = Button(self.top, text='Location登陆', command=self.log_location, state='disable')
        self.EnterLct.place(relx=0.2162, rely=0.138, relwidth=0.129, relheight=0.09)

        self.StuID = Label(self.top, text='学号：')
        self.StuID.place(relx=0.038, rely=0.26, relwidth=0.089, relheight=0.053)

        self.Stu_PWD = Label(self.top, text='密码：')
        self.Stu_PWD.place(relx=0.038, rely=0.345, relwidth=0.089, relheight=0.053)

        self.V_code = Label(self.top, text='验证码：')
        self.V_code.place(relx=0.038, rely=0.531, relwidth=0.089, relheight=0.053)

        self.IDVar = StringVar(value='')
        self.ID = Entry(self.top, textvariable=self.IDVar)
        self.ID.place(relx=0.15, rely=0.26, relwidth=0.239, relheight=0.053)

        self.PassWordVar = StringVar(value='')
        self.PassWord = Entry(self.top, textvariable=self.PassWordVar, show='*')
        self.PassWord.place(relx=0.15, rely=0.345, relwidth=0.239, relheight=0.053)
        self.PassWord.bind("<KeyPress-Return>", self.login_cmd)

        self.vcodeVar = StringVar(value='')
        self.vcode = Entry(self.top, textvariable=self.vcodeVar, state='disable')
        self.vcode.place(relx=0.15, rely=0.531, relwidth=0.239, relheight=0.053)
        self.vcode.bind("<KeyPress-Return>", self.login_cmd)

        self.Log_info = Text(self.top)
        self.Log_info.place(relx=0, rely=0.747, relwidth=0.565, relheight=0.23)
        self.Log_info.update()

        # -----------------------------------------------------------------------
        self.qk = Qiangke()
        self.qk.get_verify_code()
        self.photo = PIL.Image.open(self.qk.b_ver_code)
        self.im = PIL.ImageTk.PhotoImage(self.photo)
        self.V_Pic = Label(self.top, image=self.im)
        self.V_Pic.place(relx=0.1, rely=0.429, relwidth=0.097, relheight=0.053)
        # -----------Verify code finished by CodingDog_zxg 2019/6/18-----------

        # check button
        self.chVarDis1 = IntVar()
        self.check1 = Checkbutton(top, text="记住学号", variable=self.chVarDis1)
        self.check1.place(relx=0.24, rely=0.407, relwidth=0.1, relheight=0.053)

        self.chVarDis2 = IntVar()
        self.check2 = Checkbutton(top, text="记住密码", variable=self.chVarDis2)
        self.check2.place(relx=0.24, rely=0.469, relwidth=0.1, relheight=0.053)

        self.Login = Button(self.top, text='登录', command=self.login_cmd)
        self.Login.place(relx=0.07, rely=0.625, relwidth=0.129, relheight=0.09)

        self.Re = Button(self.top, text='刷新验证码', command=self.refresh_cmd)
        self.Re.place(relx=0.22, rely=0.625, relwidth=0.15, relheight=0.09)

        self.Email = Label(self.top, text='联系作者', fg='blue', bg='white', cursor='hand2')
        self.Email.place(relx=0.476, rely=0.933, relwidth=0.089, relheight=0.044)
        self.Email.bind("<Button-1>", lambda e: open_new("http://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=qaucodingdog@163.com"))

    # self.Log = Text(self.top)
    # self.Log.place(relx=0.038, rely=0.576, relwidth=0.565, relheight=0.409)
    # self.Log.update()


class QK(ModifyWindow):

    def __init__(self, master=None):
        ModifyWindow.__init__(self, master)
        self.filename = 'info.json'

        self.return_msg = messagebox.askquestion(title='使用前必读', message='这是一款完全开源的抢课软件 名曰抢课苟\r'
                                                                        + '仅供参考学习 请勿用来非法盈利\r'
                                                                        + '是否同意上述条件？')

        if not self.return_msg == 'yes':
            top.destroy()

        # included in __init__, try to open the dumped information file then set the Boolean type
        try:
            with open(self.filename) as f_obj:
                self.information = f_obj.read()
                self.a, self.b = self.information.split('#')[0][1:], self.information.split('#')[1][:-1]
                self.IDVar.set(value=self.a)
                self.PassWordVar.set(value=self.b)
                self.check1.select()
                self.dumped = True
        except FileNotFoundError:
            self.dumped = False

    # 登陆按钮的target
    def login_cmd(self):
        self.check1_checked = self.chVarDis1.get() == 1
        self.check2_checked = self.chVarDis2.get() == 1
        self.idinfo = self.ID.get()
        self.pwinfo = self.PassWord.get()

        # judge whether the IntVars are blank
        if not self.idinfo or not self.pwinfo:
            messagebox.showwarning(title='Error', message='账户和密码不能留空')
        elif self.pwinfo and self.pwinfo:
            self.t1 = Thread(target=self.tcmd_dumping)
            self.t1.start()
            self.t2 = Thread(target=self.tcmd_login)
            self.t2.start()
            self.Log_info.insert(1.0, 'Connecting...please wait...\n')
            self.Login.update()

    # 下面的两个方法是多线程的target
    def tcmd_dumping(self):
        # judge whether to dump the information
        if not self.dumped and self.check1_checked and self.check2_checked and self.idinfo and self.pwinfo:
            with open(self.filename, 'w') as f_obj:
                dump_info = self.idinfo + '#' + self.pwinfo
                json.dump(dump_info, f_obj)
        elif self.check1_checked and self.idinfo:
            with open(self.filename, 'w') as f_obj:
                dump_info = self.idinfo + '#'
                json.dump(dump_info, f_obj)
        elif self.check2_checked and not self.check1_checked:
            messagebox.showinfo(title='information', message='不能只保存密码噢！')

    def tcmd_login(self):
        account = self.ID.get()
        password = self.PassWord.get()
        # verify_code = self.vcodeVar.get()
        # self.qk.encoded_account_password(account, password)

        self.data = {
            'USERNAME': '{}'.format(account),
            'PASSWORD': '{}'.format(password),
        }

        self.qk.login(self.data)
        self.check_logsuc()
        if self.log_successfully:
            self.Paste['state'] = 'disable'

            self.EnterLct['state'] = 'disable'

    def refresh_cmd(self):
        self.qk.get_verify_code()
        self.photo = PIL.Image.open(self.qk.b_ver_code)
        self.im = PIL.ImageTk.PhotoImage(self.photo)
        self.V_Pic = Label(self.top, image=self.im)
        self.V_Pic.place(relx=0.1, rely=0.429, relwidth=0.097, relheight=0.053)

    # 检测复选框是否被选中 决定是否引用库
    # def check_ckbutton(self, checkbutton_name):
    # 	if checkbutton_name.get() == 1:
    # 		import json

    # 粘贴剪切板内容到StringVar
    def paste_info(self):
        self.paste_information = pyperclip.paste()
        if self.paste_information and len(self.paste_information) == 224:
            self.LocationvalVar.set(value=self.paste_information)
            messagebox.showinfo(title='information', message='Location长度符合预期！')
            # reset button state
            self.EnterLct = Button(self.top, text='Location登陆', command=self.log_location)
            self.EnterLct.place(relx=0.2162, rely=0.138, relwidth=0.129, relheight=0.09)
        else:
            messagebox.showwarning(title='Warning', message='Location长度不符合预期是不能通过此方法登录的')
            self.LocationvalVar.set(value=self.paste_information)

    # 赋值Location
    # def def_location(self):
    #     self.location_value = self.LocationvalVar.get()
    #     if self.location_value != '':
    #         messagebox.showinfo(title='information', message='赋值成功！')
    #     elif self.location_value == '':
    #         messagebox.showwarning(title='warning', message='不能留空Location 否则无法通过Location方式登陆')

    def log_location(self):
        location_url = self.LocationvalVar.get()
        self.qk.log_location(location_url)
        self.check_logsuc()
        self.Log_info.insert(1.0, 'Connecting...please wait...\n')
        self.Login.update()
        if self.log_successfully:
            self.Login['state'] = 'disable'

    # 检测是否登录成功
    def check_logsuc(self):
        try:
            self.logsuc_info = self.qk.after_response.text.split('\n')
            for line in self.logsuc_info:
                if '	<title>学生个人中心</title>' in line:
                    self.log_successfully = True
                    self.Log_info.insert(1.0, '登陆成功 \n')
                    self.Log_info.update()
                    break
                elif '<title>青岛农业大学综合教务管理系统-强智科技</title> ' in line:
                    self.Log_info.insert(1.0, '登陆失败 请检查账户密码无误后重试 \n')
                    self.Log_info.update()
                    break
        except NameError:
            self.Log_info.insert(1.0, '未知原因登陆失败，请重试\n')
            self.Log_info.update()

    def ins_open_txt(self):
        try:
            system("start \"\" \"inst.txt\"")
        except FileNotFoundError:
            self.Log_info.insert(1.0, '说明资源未找到\n')
            self.Log_info.update()

# -----------------------Display GIF in another tkinter window-----------------------
    def gif_class(self):
        window = Toplevel()
        window.title("理论效果")
        window.resizable = (0, 0)
        window.iconbitmap('1.ico')
        lbl = MyLabel(window, 'source.gif')
        lbl.pack(anchor="center")
        window.mainloop()

# --E-mail me method--
    def browser(self):
        open_new("http://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=qaucodingdog@163.com")


class MyLabel(Label):
    def __init__(self, mylable, filename):
        try:
            im = PIL.Image.open(filename)
        except FileNotFoundError:
            pass
        seq = []
        try:
            while 1:
                seq.append(im.resize((320, 240)).copy())
                im.seek(len(seq))  # skip to next frame
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']

        except KeyError:
            self.delay = 45

        first = seq[0].convert('RGB')
        self.frames = [PIL.ImageTk.PhotoImage(first)]

        Label.__init__(self, mylable, image=self.frames[0])

        temp = seq[0].convert('RGB')
        for image in seq[1:]:
            frame = image.convert('RGB')
            temp.paste(frame)
            self.frames.append(PIL.ImageTk.PhotoImage(temp))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)
# --------------------------Finished by CodingDog_zxg 2019/7/19--------------------------


class CheckNecessary:

    def __init__(self):
        self.check_necessary()

    def check_necessary(self):
        self.cna = Tk()
        self.cna.withdraw()
        self.r = messagebox.askokcancel('info', '一定要先连接VPN！ \r 请确认VPN连接完毕以后关闭此窗口！')


cn = CheckNecessary()
# print(cn.r)
if cn.r:
    cn.cna.deiconify()
    cn.cna.destroy()
    top = Tk()
    top.resizable(0, 0)
    top.iconbitmap('1.ico')
    canvas = Canvas(top, width=640, height=480, bg='#E6E6E6')
    QK(top).mainloop()
