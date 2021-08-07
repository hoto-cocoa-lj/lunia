import win32gui, win32ui, win32con,time,random
from ctypes import windll
from PIL import Image
from lunia import astar
import cv2,lunia.constant as lc,lunia.accessorytool as la
import numpy as np,lunia.pictool as lp,lunia.luniatool as lt


at=la.AccessoryTool()
wds=at.wds
wdposes=at.wdposes
keycode_1=3*16+1
scanCode_1=2

def progress_召唤_一个乐师(i,jiaxueFlg=True,wds=wds):
    time.sleep(.3)
    win32gui.SetForegroundWindow(wds[i])
    time.sleep(.2)
    if jiaxueFlg:
        time.sleep(6.5)

        lt.key_click(keycode=keycode_1,relay1=.01,relay2=.1,scanCode=scanCode_1)

        time.sleep(3)
    lt.key_click(keycode=scanCode_1+1,relay1=.01,relay2=.1,scanCode=scanCode_1+1)

    time.sleep(16)
    lt.key_click(keycode=scanCode_1+2,relay1=.01,relay2=.1,scanCode=scanCode_1+2)

def progress_召唤_n个乐师(n=4):
    s=input('请输入开始的窗口序号：\n')
    i=0 if not s else int(s.strip())-1

    progress_召唤_一个乐师(i,False)
    while 1:
        t1 = time.time()
        i=(i+1)%n
        progress_召唤_一个乐师(i,True)
        print(time.time()-t1)

if __name__=='__main__':
    progress_召唤_n个乐师()
