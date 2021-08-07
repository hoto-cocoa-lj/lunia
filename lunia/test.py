import win32gui, win32ui, win32con,time,random
from ctypes import windll
from PIL import Image
from lunia import astar
import cv2,lunia.constant as lc,lunia.accessorytool as la
import numpy as np,lunia.pictool as lp,lunia.luniatool as lt

def getMyPos(poslist):
    for pos in poslist:
        if (pos[0]-1,pos[1]) in poslist and (pos[0]+1,pos[1]) in poslist\
                and (pos[0],pos[1]-1) in poslist and (pos[0],pos[1]+1) in poslist:
            return pos

def getGameMap(img,fp,index=0):
    cnts,imgBW=lp.getContours(img=img,thresh=lc.smallMapThreshold,inv=0)
    imga=np.zeros((img.shape[0],img.shape[1]), np.uint8)
    _,_,cnt=lp.getContourByIndex(cnts,0)
    cv2.drawContours(imga,[cnt],0,255,thickness=-1)
    # lp.showImg(imga)
    # lp.showImg(imgBW)
    # cv2.drawContours(img,[cnt],0,(0,0,255),thickness=-1)
    imga=np.minimum(imga,imgBW)
    # lp.showImg(imga)
    cv2.imwrite(fp,imga)

def move1(start=None,end=None):
    p0=start
    lastp0=None
    stopTimes=0
    while 1:
        img1 = lp.captureWindow(hWnd)
        img = lp.getPicClip(img1, smp)
        poslist = lp.getPosByColorGray(img, 255)
        p0 = getMyPos(poslist)
        disx,disy=end[0]-p0[0],end[1]-p0[1]
        if abs(disx)+abs(disy)<=3:
            return

        arrow=None
        if abs(disx)>abs(disy):
            if disx<0:
                arrow=lc.upKey
            else:
                arrow = lc.downKey
        else:
            if disy<0:
                arrow=lc.leftKey
            else:
                arrow = lc.rightKey
        if lastp0 ==p0:
            stopTimes +=1
            if stopTimes>2:
                lt.key_click(keycode=0, scanCode=lc.leftKey, relay1=0,relay2=0.3)
                lt.key_click(keycode=0, scanCode=lc.upKey, relay1=0,relay2=0.3)
                stopTimes = 0
        elif abs(disx) + abs(disy) <= 5:
            lt.key_click(keycode=0, scanCode=arrow, relay1=0,relay2=0.3)
            stopTimes = 0
        else:
            lt.key_click(keycode=0, scanCode=arrow,relay1=0,relay2=0.1)
            lt.key_click(keycode=0, scanCode=arrow,relay1=0,relay2=0.1)
            time.sleep(.5)
            stopTimes = 0
        print(lastp0,p0,end,lc.arrowMap[arrow])
        lastp0 =p0

def move(start=None,end=None):
    p0=start
    lastp0=None
    stopTimes=0
    arrow = None

    while 1:
        walkFlg = False
        img1 = lp.captureWindow(hWnd)
        img = lp.getPicClip(img1, smp)
        poslist = lp.getPosByColorGray(img, 255)
        p0 = getMyPos(poslist)
        disy,disx=end[0]-p0[0],end[1]-p0[1]
        if abs(disx)+ abs(disy)<=2:
            return

        if stopTimes>1:
            if arrow==lc.leftKey or arrow==lc.rightKey:
                arrow=lc.upKey if disy<0 else lc.downKey
            else:
                arrow = lc.leftKey if disx < 0 else lc.rightKey
            stopTimes =0
            walkFlg=True
        else:
            if abs(disx)>abs(disy):
                if disx<0:
                    arrow=lc.leftKey
                else:
                    arrow = lc.rightKey
            else:
                if disy<0:
                    arrow=lc.upKey
                else:
                    arrow = lc.downKey

        if lastp0 ==p0:
            stopTimes +=1
        if abs(disx) + abs(disy) <= 4 or walkFlg:
            print('walk')
            lt.key_click(keycode=0, scanCode=arrow, relay1=0,relay2=0.3)
            time.sleep(.2)
        else:
            print('run')
            lt.key_click(keycode=0, scanCode=arrow,relay1=0,relay2=0)
            lt.key_click(keycode=0, scanCode=arrow,relay1=0,relay2=0)
            # stopTimes=0
            time.sleep(.1)
        print(lastp0,p0,end,lc.arrowMap[arrow],stopTimes)
        lastp0 =p0

fp = 'E:\picmodify\lunia\pic\capture/1.bmp'

t1=time.time()
at=la.AccessoryTool()
hWnd=at.wds[0]
smp=lc.smallMapPos
smp=lc.SMP
img1=lp.captureWindow(hWnd)
img=lp.getPicClip(img1,smp)
cv2.imwrite('E:\picmodify\lunia\pic\capture/3.bmp', img)
# img=cv2.imread(fp)
getGameMap(img,fp,0)


poslist=lp.getPosByColorGray(img,255)
p0=getMyPos(poslist)
p0=p0[0]+1,p0[1]+1
print(p0)

p1=(42,60)
time.sleep(1)
win32gui.SetForegroundWindow(hWnd)
time.sleep(1)


# from_pos = [63,44]
from_pos = p0
# target_pos = (79, 49)       #废弃光山start
target_pos = (77,99)    #废弃光山end
# target_pos = (70, 60) #魔1二路

# corners=[(71,51),(77,51),(77,73),(84,73)] #mo5
# corners=[(82,51),(88,51),(88,73),(95,73),(95,51)] #mo2
# corners=[(82,51),(88,51),(88,73),(95,73)] #mo1
# corners=astar.main(fp, from_pos, target_pos)
corners=[(82,51),(88,51),(88,73),(95,73),(95,51)] #mo2
print('corners:',corners)

imgcopy=img.copy()
fix=1
if corners:
    for c in corners:
        imgcopy[c[0]-fix:c[0]+fix,c[1]-fix:c[1]+fix]=(0,0,255,0)
    cv2.imwrite('E:\picmodify\lunia\pic\capture/2.jpg', imgcopy)
    t2=time.time()
    for c in corners:
        move(end=c)
print(time.time()-t1)
print(time.time()-t2)