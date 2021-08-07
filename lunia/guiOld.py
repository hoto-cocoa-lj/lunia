import tkinter as tk,lunia.constant as lc
import lunia.luniatool as ll,os
from tkinter import messagebox,ttk

def seeLog():
    os.system('notepad {}/{}'.format(os.getcwd(),lc.logFile))

wd = tk.Tk()
wd.title("HOTO COCOA")
wd.geometry("750x250")

# fontType="楷体"
fontType=None
fontSize=12
font_=(fontType,fontSize)

#checkbox frame
chbFM = tk.Frame()
chbVars=[]
chbs=[]
for i in range(len(lc.ATTRS)):
    chbVars.append(tk.IntVar())
    c='red' if i%2 else 'green'
    chb=tk.Checkbutton(chbFM, text=lc.ATTRS[i], variable=chbVars[i],fg=c)
    chbs.append(chb)
    chb.pack(side=tk.LEFT)
    if lc.zjdDict['rows'].count(i+1):
        chb.select()
chbVSH=tk.IntVar()
chbSH=tk.Checkbutton(chbFM, text='神话装备', variable=chbVSH,fg='blue')
chbSH.pack(side=tk.LEFT)
if lc.zjdDict['sh']:chbSH.select()
chbFM.pack()


#zjdDict={'target':1.5,'rows':(2, 3),'sh':1}
inputFM1 = tk.Frame(wd)

logButton = tk.Button(inputFM1, text='查看记录', command=seeLog)
logButton.pack(side=tk.LEFT)

tk.Label(inputFM1, text="请输入要购买或提取个数，只接受整数").pack( side=tk.LEFT)
countInput = tk.Entry(inputFM1, bd =5)
countInput.pack(side=tk.LEFT)
inputFM1.pack()

inputFM2 = tk.Frame(wd)
tk.Label(inputFM2, text="请输入目标值，只接受数字，如需要1.5顶及以上时输入1.5").pack( side=tk.LEFT)
targetInput = tk.Entry(inputFM2, bd =5)
targetInput.pack(side=tk.LEFT)
inputFM2.pack()

inputFM3 = tk.Frame(wd)
tk.Label(inputFM3, text="请选择你需要测试的阈值，不测试可忽略").pack( side=tk.LEFT)
comvalue = tk.StringVar()  # 窗体自带的文本，新建一个值
comboxlist = ttk.Combobox(inputFM3, textvariable=comvalue)  # 初始化
comboxlist["values"] = ("1:再鉴定", "2:再鉴定商店", "3:包裹条")
comboxlist.current(0)  # 选择第一个
comboxlist.pack(side=tk.LEFT)
inputFM3.pack()


outputFM = tk.Frame(wd)
textbox = tk.Text(outputFM, height =5)
textbox.pack()
outputFM.pack()



def showmsgInTextbox(msg):      #用textbox显示文本会遇到阻塞问题，改用对话框
    textbox.delete('1.0','end')
    textbox.insert('end',msg)

def showmsg(msgs):
    m=''
    for i in msgs:
       m+=i+'\n'
    return messagebox.askokcancel(title='程序执行中...', message=m)

def show(inp):
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
        return showmsg(msgs)

def handleButton(k):
    count=countInput.get()
    target=targetInput.get()
    sh=chbVSH.get()
    yuzhi=comboxlist.get()[0]
    rows=[]
    for i in range(len(chbVars)):
        if chbVars[i].get():
            rows.append(i+1)

    if k in list('126'):
        try:
            count = int(count)
        except ValueError as e:
            messagebox.showerror(title='输入错误', message='请在购买或提取个数输入框里输入整数')
            countInput.focus()
            return
    if k=='4':
        try:
            target = float(target)
        except ValueError as e:
            messagebox.showerror(title='输入错误', message='请鉴定目标值输入框里输入数字')
            targetInput.focus()
            return
    # print(type(k),type(count),type(target),type(sh),type(rows))
    # t=Thread(target=show,args=(k))
    # t.start()
    if show(k):
        ll.main2(k,count,target,sh,rows,yuzhi)
    else:
        showmsgInTextbox('你已取消操作')



#zjdDict={'target':1.5,'rows':(2, 3),'sh':1}
actionFM = tk.Frame()
actionBts=[]
for k in lc.actions:
    text=k+':'+lc.actions[k]
    # b=tk.Button(actionFM,text=text, command=lambda:handleButton(k))
    b=tk.Button(actionFM,text=text)
    actionBts.append(b)
    b.pack(side=tk.LEFT)

#lambda里冒号右边的变量会实时取值，所以貌似不能用循环
actionBts[0].bind('<Button-1>',lambda x:handleButton('1'))
actionBts[1].bind('<Button-1>',lambda x:handleButton('2'))
actionBts[2].bind('<Button-1>',lambda x:handleButton('3'))
actionBts[3].bind('<Button-1>',lambda x:handleButton('4'))
actionBts[4].bind('<Button-1>',lambda x:handleButton('5'))
actionBts[5].bind('<Button-1>',lambda x:handleButton('6'))
actionBts[6].bind('<Button-1>',lambda x:handleButton('8'))
actionBts[7].bind('<Button-1>',lambda x:handleButton('9'))
actionFM.pack()



wd.mainloop()
#显示窗口

