import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2,lunia.constant as lc,lunia.accessorytool as la
import numpy as np,lunia.pictool as lp

at=la.AccessoryTool()

def getSmallMapPos():
    # at=la.AccessoryTool()
    hWnd=at.wds[0]
    #只取图片的右上角识别小地图
    left,up=600,50
    # img=at.captureWindow(0,(0,0),(width,height))
    # img=np.asarray(img)
    img1=lp.captureWindow(hWnd)
    img=img1[up:220,left:]
    cnts=lp.getContours(img=img)
    pos1,pos2,cnt=lp.getContourByIndex(cnts,0)

    a,b=left+pos1[0],up+pos1[1]
    c,d=left+pos2[0],up+pos2[1]
    print((a,b),(c,d))
    cv2.rectangle(img1,(a,b),(c,d),(0,0,255),1)
    cv2.imshow("img", img1);cv2.waitKey(0)
getSmallMapPos()