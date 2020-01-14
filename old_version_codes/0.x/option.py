from tkinter import *

#初始化Tk()
myWindow=Tk()
myWindow.title('Python GUI Learning')
v=IntVar()
#列表中存储的是元素是元组
language=[('python',0),('C++',1),('C',2),('Java',3)]
#定义单选按钮的响应函数
def callRB():
    for i in range(4):
        if (v.get()==i):
            root1 = Tk()
            Label(root1,text='你的选择是'+language[i][0]+'!',fg='red',width=20,height=6).pack()
            Button(root1,text='确定',width=3,height=1,command=root1.destroy).pack(side='bottom')

Label(myWindow,text='选择一门你喜欢的编程语言').pack(anchor=W)

#for循环创建单选框
for lan,num in language:
    Radiobutton(myWindow, text=lan, value=num, command=callRB, variable=v).pack(anchor=W)
#进入消息循环
myWindow.mainloop()
