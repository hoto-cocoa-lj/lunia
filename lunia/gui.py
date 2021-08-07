import tkinter as tk,lunia.constant as lc
import lunia.luniatool as ll,os,win32con,win32gui,time
from tkinter import messagebox,ttk

class LuniaGUI:
    fontType = None
    fontSize = 12
    font_ = (fontType, fontSize)


    #当tk窗口在最上层(准确的说是处于激活状态)时，经常出现按printscreen无效的bug，
    #截图前用shiftWindow隐藏tk窗口，之后重新激活来解决此bug。bug原因不明。
    def shiftWindow(self,state):
        a = win32gui.FindWindow(None,lc.windowName)
        # print('{}窗口的句柄是{}'.format(lc.windowName,a))
        time.sleep(.1)
        # win32gui.ShowWindow(a, win32con.SW_HIDE)
        win32gui.ShowWindow(a, state)


    def __init__(self):
        self.wd = tk.Tk()
        self.wd.title(lc.windowName)
        self.wd.geometry("750x250")
        # fontType="楷体"


        # checkbox frame
        self.chbFM = tk.Frame()
        self.chbVars = []
        self.chbs = []
        for i in range(len(lc.ATTRS)):
            self.chbVars.append(tk.IntVar())
            c = 'red' if i % 2 else 'green'
            chb = tk.Checkbutton(self.chbFM, text=lc.ATTRS[i], variable=self.chbVars[i], fg=c)
            self.chbs.append(chb)
            chb.pack(side=tk.LEFT)
            if lc.zjdDict['rows'].count(i + 1):
                chb.select()
        self.chbVSH = tk.IntVar()
        self.chbSH = tk.Checkbutton(self.chbFM, text='神话装备', variable=self.chbVSH, fg='blue')
        self.chbSH.pack(side=tk.LEFT)
        if lc.zjdDict['sh']: self.chbSH.select()
        self.chbFM.pack()

        # zjdDict={'target':1.5,'rows':(2, 3),'sh':1}
        self.inputFM1 = tk.Frame(self.wd)

        self.logButton = tk.Button(self.inputFM1, text='查看记录', command=self.seeLog)
        self.logButton.pack(side=tk.LEFT)

        tk.Label(self.inputFM1, text="请输入要购买或提取个数，只接受整数").pack(side=tk.LEFT)
        self.countInput = tk.Entry(self.inputFM1, bd=5)
        self.countInput.pack(side=tk.LEFT)
        self.inputFM1.pack()

        self.inputFM2 = tk.Frame(self.wd)
        tk.Label(self.inputFM2, text="请输入目标值，只接受数字，如需要1.5顶及以上时输入1.5").pack(side=tk.LEFT)
        self.targetInput = tk.Entry(self.inputFM2, bd=5)
        self.targetInput.pack(side=tk.LEFT)
        self.inputFM2.pack()

        self.inputFM3 = tk.Frame(self.wd)
        tk.Label(self.inputFM3, text="请选择你需要测试的阈值，不测试可忽略").pack(side=tk.LEFT)
        self.comvalue = tk.StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = ttk.Combobox(self.inputFM3, textvariable=self.comvalue)  # 初始化
        self.comboxlist["values"] = ("1:再鉴定", "2:再鉴定商店", "3:包裹条")
        self.comboxlist.current(0)  # 选择第一个
        self.comboxlist.pack(side=tk.LEFT)
        self.inputFM3.pack()

        self.outputFM = tk.Frame(self.wd)
        self.textbox = tk.Text(self.outputFM, height=5)
        self.textbox.pack()
        self.outputFM.pack()

        # zjdDict={'target':1.5,'rows':(2, 3),'sh':1}
        self.actionFM = tk.Frame()
        self.actionBts = []
        for k in lc.actions:
            text = k + ':' + lc.actions[k]
            # b=tk.Button(actionFM,text=text, command=lambda:handleButton(k))
            b = tk.Button(self.actionFM, text=text)
            self.actionBts.append(b)
            b.pack(side=tk.LEFT)

        # lambda里冒号右边的变量会实时取值，所以貌似不能用循环
        self.actionBts[0].bind('<Button-1>', lambda x: self.handleButton('1'))
        self.actionBts[1].bind('<Button-1>', lambda x: self.handleButton('2'))
        self.actionBts[2].bind('<Button-1>', lambda x: self.handleButton('3'))
        self.actionBts[3].bind('<Button-1>', lambda x: self.handleButton('4'))
        self.actionBts[4].bind('<Button-1>', lambda x: self.handleButton('5'))
        self.actionBts[5].bind('<Button-1>', lambda x: self.handleButton('6'))
        self.actionBts[6].bind('<Button-1>', lambda x: self.handleButton('8'))
        self.actionBts[7].bind('<Button-1>', lambda x: self.handleButton('9'))
        self.actionFM.pack()



    def run(self):
        self.wd.mainloop()
        # 显示窗口

    def seeLog(self):
        os.system('notepad {}/{}'.format(os.getcwd(),lc.logFile))
    
    
    
    def showmsgInTextbox(self,msg):      #用textbox显示文本会遇到阻塞问题，改用对话框
        self.textbox.delete('1.0','end')
        self.textbox.insert('end',msg)
    
    def showmsg(self,msgs):
        m=''
        for i in msgs:
           m+=i+'\n'
        return messagebox.askokcancel(title='程序执行中...', message=m)
    
    def show(self,inp):
        msgs=None
        if inp == '1':  # 买东西
            msgs=lc.waitmsg, lc.buymsg1
        elif inp == '2':  # 提取商品
            msgs=lc.waitmsg, lc.tiqumsg1
        elif inp == '3':  # 合并背包的再鉴定
            msgs=lc.waitmsg, lc.hebingmsg1
        elif inp == '5':  # 合并所有背包的再鉴定
            msgs=lc.waitmsg, lc.hebingmsg1
        elif inp == '6':  # 1+2+5
            msgs=lc.buy_tiqu_hebingall_msg1,lc.waitmsg, lc.buymsg1
        elif inp == '4':  # 再鉴定
            msgs=lc.waitmsg, lc.zjdmsg1
        elif inp == '8':  # 测试要检索图片的阈值
            msgs=lc.waitmsg, lc.yzmsg1
        elif inp == '9':  # 测量距离
            msgs=lc.waitmsg,lc.measuremsg1
        if msgs:
            # showmsgInTextbox(msgs)
            return self.showmsg(msgs)
    
    def handleButton(self,k):
        count=self.countInput.get()
        target=self.targetInput.get()
        sh=self.chbVSH.get()
        yuzhi=self.comboxlist.get()[0]
        rows=[]
        for i in range(len(self.chbVars)):
            if self.chbVars[i].get():
                rows.append(i+1)
    
        if k in list('126'):
            try:
                count = int(count)
            except ValueError as e:
                messagebox.showerror(title='输入错误', message='请在购买或提取个数输入框里输入整数')
                self.countInput.focus()
                return
        if k=='4':
            try:
                target = float(target)
            except ValueError as e:
                messagebox.showerror(title='输入错误', message='请鉴定目标值输入框里输入数字')
                self.targetInput.focus()
                return
        # print(type(k),type(count),type(target),type(sh),type(rows))
        # t=Thread(target=show,args=(k))
        # t.start()
        if self.show(k):
            self.shiftWindow(win32con.SW_HIDE)
            ll.main2(k,count,target,sh,rows,yuzhi)
            self.shiftWindow(win32con.SW_SHOWNOACTIVATE)

        else:
            self.showmsgInTextbox('你已取消操作')
    
if __name__=='__main__':
    LuniaGUI().run()
    
