import cv2, numpy as np, lunia.constant as lc, lunia.log as ll
import win32api, win32con, time,win32gui,win32ui
from PIL import ImageGrab
from ctypes import *


PICDIR = lc.PICDIR
RESULTJPG = lc.RESULTJPG
RESULT2JPG = lc.RESULT2JPG
SCREENJPG = lc.SCREENJPG
SHORTTIME = lc.SHORTTIME = .1
ATTRS = lc.ATTRS
shenhuaPoints = lc.shenhuaPoints
puguanPoints = lc.puguanPoints

# 再鉴定的项目的区域大小(w1*h)
# 再鉴定的数值的区域大小(w2*h)
w1, w2, h = lc.w1, lc.w2, lc.h

def emptyClipboard():
    windll.user32.OpenClipboard(c_int(0))
    windll.user32.EmptyClipboard()
    windll.user32.CloseClipboard()

def showImg(img):
    cv2.imshow("img", img);cv2.waitKey(0)

def getPosByColorGray(img,color=255):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return list(zip(*np.where(img==color)))

def getContours(imgname=None, img=None, cvtOneChannel=True, thresh=10, inv=True, cvtTh=True,doOpen=False,doClose=False):
    img=img.copy()
    if imgname:
        img = cv2.imread(imgname)
    if cvtOneChannel:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = img[:,:,2]
    if cvtTh:
        mode = cv2.THRESH_BINARY_INV if inv else cv2.THRESH_BINARY
        _, img = cv2.threshold(img, thresh, 255, mode)
    if doOpen:
        k = np.ones((3, 3), np.uint8)
        # k=cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, k)
    # showImg(img)
    if doClose:
        ksize=3
        k = np.ones((ksize, ksize), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, k)
    # showImg(img)

    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return contours,img

def getPicClip(img,clip):
    return img[clip[0][1]:clip[1][1], clip[0][0]:clip[1][0]]

def getContourByIndex(contours, index=0):
    contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
    return contours[index][0][0], contours[index][2][0],contours[index]

def captureWindow(hWnd):
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top

    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    im_opencv = np.frombuffer(signedIntsArray, dtype = 'uint8')
    im_opencv.shape = (height, width, 4)
    # cv2.imwrite(lc.CAPTUREDIR+"im_opencv.jpg",im_opencv) #保存
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd, hWndDC)
    return im_opencv

#全屏截图1
def printscreen1():
    emptyClipboard()
    while 1:
        time.sleep(.1)
        win32api.keybd_event(win32con.VK_SNAPSHOT, 0)
        time.sleep(.3)
        image = ImageGrab.grabclipboard()  # 获取剪贴板文件
        if image != None:
            return image
        else:
            ll.e('printscreen在剪贴板找不到屏幕截图')

#全屏截图
def printscreen():
    emptyClipboard()
    while 1:
        time.sleep(.2)
        image = ImageGrab.grab()
        time.sleep(.2)
        # image.show()
        if image != None:
            return image
        else:
            ll.e('printscreen截图失败')

#在全屏截图里寻找template，返回坐标列表
#threshold：阈值，低于此值的不返回
#istest：是否是测试，True时会打印最高的几处的相似度，供参考修改阈值
#若此函数没有找到template，istest会变成True
#onlymax：True时只返回相似度最高的一处
#tname：template的名字/路径，仅供print使用
def findTemplateInPic(template, threshold,
                      istest=False, onlymax=False, tname=None):
    if tname:
        ll.i('>' * 11 + '将在图片中搜索{}模板\n'.format(tname))
    img = printscreen()
    src = np.array(img, np.uint8).reshape(img.size[1], img.size[0], -1)
    # src = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], -1)

    # 本来在这里把src从BGR转RGB，但每个图都要转，所以改成把template从RGB转BGR
    # src= cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    # cv2.imshow('result', src)
    # cv2.waitKey(0)

    methods = [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF,
               cv2.TM_CCOEFF_NORMED]
    res = cv2.matchTemplate(src, template, methods[-1])

    loc = np.where(res >= threshold)
    if len(loc[0]) == 0:
        istest = True
    if onlymax:
        maxloc = np.where(res == np.max(res))
        # ll.i('maxloc=',maxloc)
        returnLoc = list(zip(*maxloc[::-1]))
        ll.i('<' * 11 + 'findTemplateInPicOnlymax找到{}个对象，坐标是{}\n'.format(len(returnLoc), returnLoc))
        return returnLoc, src

    # matchTemplate经常在目标附近(差几个像素)找到很多匹配，
    # 把横纵坐标差距的和 不到半个template宽/高 的匹配项只保留1个
    L_ = list(zip(*loc[::-1]))
    if len(L_) > 1:
        offset = min(template.shape[0] / 2, template.shape[1] / 2)
        returnLoc = [L_[0]]
        for i in range(1, len(L_)):
            _flg = True
            for j in returnLoc:
                s1 = abs(L_[i][0] - j[0])
                s2 = abs(L_[i][1] - j[1])
                if s1 + s2 < offset:
                    _flg = False
                    break
            if _flg: returnLoc.append(L_[i])
    else:
        returnLoc = L_

    ll.i('<' * 11 + 'findTemplateInPic找到{}个对象，坐标是{}\n'.format(len(returnLoc), returnLoc))

    # 下面这段代码用来观察threshold应该取什么值
    if istest:
        resf = res.flatten()
        # ll.i(np.max(resf))
        resfs = resf.argsort()[::-1]
        ll.i('最匹配的若干项的相似度是{}'.format(resf[resfs[0:10]]))
        tshp = template.shape
        for pt in zip(*loc[::-1]):  # 保存识别结果图片
            cv2.rectangle(src, pt, (pt[0] + tshp[1], pt[1] + tshp[0]), (0, 255, 0), 2)
        cv2.imwrite(PICDIR + RESULTJPG, src)

    return returnLoc, src


# 再鉴定的主要逻辑，放错地方不改了
# pt:商城的位置，根据此位置分析鉴定结果。只需找一次
def reJD(template, pt=None, rows=lc.zjdDict['rows'], cols=range(1,9), isShenhua=True, tname=lc.ZJDSHOPPATH):
    if pt == None:
        loc, src = findTemplateInPic(template, threshold=lc.zjdShopThreshold, tname=tname)
        assert len(loc) > 0, '没找到鉴定商店，请重新操作'
        shp = template.shape
        pt = loc[0][0] + w1, loc[0][1] + shp[0]
    else:
        img = printscreen()

        # src = np.array(img.getdata(), np.uint8)
        #np.array(img, np.uint8)比np.array(img.getdata(), np.uint8)快10s
        #但img.getdata()本身只要不到1s
        src = np.array(img, np.uint8).reshape(img.size[1], img.size[0], -1)

    points = shenhuaPoints if isShenhua else puguanPoints

    # res=[]

    rows___ = range(1, 9)
    # 本次得分，从左边开始取像素的范围
    point, offset = [0,0], 4

    # for j in rows:
    for j in rows___:
        for i in cols:
            left, right = pt[0] + w2 * (i - 1), pt[0] + w2 * i
            up, down = pt[1] + h * (j - 1), pt[1] + h * j

            # area=src[up:down,left:right,3]
            # 以前用整个区域，收到白色数字影响较大，换成没字的地方
            # 以前用rgb三通道，改用r单通道
            area = src[up + offset:down - offset, left:left + offset, 0]
            # print(area.shape)
            m = round(np.mean(area), 2)

            str_ = '\t{}鉴定{}{}级,颜色均值{}'

            # print(str_.format(ATTRS[j - 1], '', i, m))
            # continue

            isPointRow,xishu = rows.count(j),0

            if m > lc.COLOR_LEVEL_4:
                pass
            elif m > lc.COLOR_LEVEL_3:
                xishu=3
                ll.i(str_.format(ATTRS[j - 1], '3个', i, m))
            elif m > lc.COLOR_LEVEL_2:
                xishu=2
                ll.i(str_.format(ATTRS[j - 1], '2个', i, m))
            elif m > lc.COLOR_LEVEL_1:
                xishu=1
                ll.i(str_.format(ATTRS[j - 1], '', i, m))

            if isPointRow:
                point[0] += points[i - 1] * xishu
            else:
                point[1] += points[i - 1] * xishu
            # res.append(m)
            # cv2.rectangle(src, (left,up), (right, down),(0,255,0),1)
    # res.sort()
    # print(res[::-1][:4])
    # cv2.imwrite(PICDIR+RESULT2JPG, src)
    return pt, point

#返回背包的坐标集合
def getBagsPosition():
    bags = cv2.imread(PICDIR + lc.BAGSPATH, 1)
    template = cv2.cvtColor(bags, cv2.COLOR_RGB2BGR)
    locs, src = findTemplateInPic(template, istest=1,
                                  threshold=lc.bagsThreshold, onlymax=True, tname=lc.BAGSPATH)

    loc = locs[0]
    w, h = int(bags.shape[1] / 7), bags.shape[0]
    fix = int(w / 2)
    pos = []
    for i in range(7):
        left, right = loc[0] + i * w, loc[0] + i * w + w
        up, down = loc[1], loc[1] + h
        area = src[up:down, left:right, 2]
        m = round(np.mean(area), 2)
        # print(m)
        if m < 70:
            pos.append([left + fix, up + fix])
    #     cv2.rectangle(src, (left, up), (right, down), (0, 0, 255), 2)
    # cv2.imwrite(PICDIR+RESULT2JPG, src)
    return pos


if __name__ == "__main__":
    zjd = cv2.imread(PICDIR + lc.ZJDPATH, 1)
    zjd_shop = cv2.imread(PICDIR + lc.ZJDSHOPPATH, 1)
    bags = cv2.imread(PICDIR + lc.BAGSPATH, 1)
    template1 = cv2.cvtColor(zjd, cv2.COLOR_RGB2BGR)
    template2 = cv2.cvtColor(zjd_shop, cv2.COLOR_RGB2BGR)
    template3 = cv2.cvtColor(bags, cv2.COLOR_RGB2BGR)
    findTemplateInPic(template1,threshold=lc.zjdThreshold,istest=1,tname=lc.ZJDPATH)
    # findTemplateInPic(template2,threshold=lc.zjdShopThreshold,tname=lc.ZJDSHOPPATH)
    # findTemplateInPic(template3,threshold=lc.bagsThreshold,istest=1,tname=lc.BAGSPATH)
    # pt = reJD(template2, isShenhua=1)
    # getBagsPosition()
