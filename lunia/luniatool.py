import win32api, win32con, time, cv2, threading, lunia.log as ll
import lunia.pictool as lp, lunia.constant as lc



PICDIR = lc.PICDIR
ZJD = cv2.imread(PICDIR + lc.ZJDPATH, 1)
ZJDSHOP = cv2.imread(PICDIR + lc.ZJDSHOPPATH, 1)
BAGS = cv2.imread(PICDIR + lc.BAGSPATH, 1)
SHORTTIME = lc.SHORTTIME
F1CODE = lc.F1CODE
F2CODE = lc.F2CODE
shenhuaPoints = lc.shenhuaPoints
puguanPoints = lc.puguanPoints
EQTYPES = lc.EQTYPES
ATTRS = lc.ATTRS
ZJDLOSS = lc.ZJDLOSS


def movZJDAll(threshold=lc.zjdThreshold):
    #包裹图标的坐标
    pos = lp.getBagsPosition()
    ll.i('发现需要合并的包裹{}个'.format(len(pos)))
    zjdPos = []

    #遍历包裹，移动再鉴定，并记录每页最后一处再鉴定的坐标
    for p in pos:
        time.sleep(SHORTTIME * 2)
        win32api.SetCursorPos(p)
        time.sleep(SHORTTIME * 2)
        mouse_click()

        time.sleep(SHORTTIME * 3)
        res=movZJD(threshold)
        zjdPos.append(res)

    time.sleep(SHORTTIME * 2)
    on = False  # on表示物品是否是点起状态

    #判断最后一页是否有再鉴定，作相应处理
    if zjdPos[-1] != None:
        on = True
        time.sleep(SHORTTIME * 2)
        win32api.SetCursorPos(zjdPos[-1])
        time.sleep(SHORTTIME * 4)
        mouse_click()

    #翻页移动再鉴定
    for j in range(len(pos) - 2, -1, -1):
        if zjdPos[j] != None:
            time.sleep(SHORTTIME * 2)
            win32api.SetCursorPos(pos[j])
            time.sleep(SHORTTIME * 4)
            mouse_click()

            time.sleep(SHORTTIME * 2)
            win32api.SetCursorPos(zjdPos[j])
            time.sleep(SHORTTIME * 4)
            mouse_click()

            if on:
                time.sleep(SHORTTIME * 7)
                mouse_click()
            else:
                on = True


def movZJD(threshold=lc.zjdThreshold):  # 单页内移动再鉴定
    ZJDshp = ZJD.shape
    template = cv2.cvtColor(ZJD, cv2.COLOR_RGB2BGR)

    #找到页内所有的再鉴定的左上角坐标
    pts, _ = lp.findTemplateInPic(template, threshold=threshold, tname=lc.ZJDPATH)

    #加上再鉴定的一半的size
    pts = [(int(a + ZJDshp[1] / 2), int(b + ZJDshp[0] / 2)) for a, b in pts]

    #把最后一个坐标作为集合点
    if len(pts) > 1:
        moveobj(pts[:-1], pts[-1])
    else:
        ll.w('movZJD只找到{}个对象，本次不进行合并'.format(len(pts)))
    return pts[-1] if len(pts) >= 1 else None


# 移动objs的东西到target
# objs:起点坐标列表，如[(1,1),(33,36)]，target:终点坐标，如(11,11)
def moveobj(objs, target):
    for x, y in objs:
        # if lc.exitFlg: return
        time.sleep(SHORTTIME * 2)
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(SHORTTIME * 2)
        win32api.SetCursorPos(target)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 测量两个点的像素(?)距离，供SetCursorPos使用
# 似乎和微信的截图工具的数值一样，可以用那个
def measureDistance():
    input(lc.measureDistanceStr1)
    pos1 = win32api.GetCursorPos()
    input(lc.measureDistanceStr2)
    pos2 = win32api.GetCursorPos()
    print(pos1, pos2, pos2[0] - pos1[0], pos2[1] - pos1[1])
    return pos2[0] - pos1[0], pos2[1] - pos1[1]


# 从商城提取区提取物品到背包，光标移动到商城提取区的物品调用此方法
# 内部操作：双击物品再f1确定
def takeItem(times=1):
    while times > 0:
        # if lc.exitFlg: return
        time.sleep(SHORTTIME * 5)
        mouse_click(times=2)  # 点列表页面购买键

        key_click(keycode=F1CODE, relay1=SHORTTIME * 15)  # 点f1确定


        times -= 1
    key_click(lc.ESCCODE,relay1=1,scanCode=lc.ESCSCANCODE)



# 买东西:把光标移动到商品列表界面的商品的购买按钮上调用此方法
# 内部操作：单击购买，商品页面再点购买，f1确定，f2取消提取
# fix:从列表购买键到商品页面购买键的距离，可用measureDistance计算
# times:买几次
def buy(fix=lc.FIX1, times=1):
    if fix == None:
        fix = measureDistance()
    while times > 0:
        # if lc.exitFlg: return
        time.sleep(SHORTTIME)
        mouse_click()  # 点列表页面购买键

        time.sleep(SHORTTIME * 10)
        pos = win32api.GetCursorPos()
        pos = int(pos[0]) + fix[0], int(pos[1]) + fix[1]
        win32api.SetCursorPos(pos)  # 移动到商品页面购买键
        time.sleep(SHORTTIME)
        mouse_click()  # 点商品页面购买键

        #回答是否购买
        key_click(keycode=F1CODE, relay1=SHORTTIME * 8)  # 点f1确定

        #是否提取商品回答
        if times == 1:
            key_click(keycode=F1CODE, relay1=SHORTTIME * 8)  # 点f1确定
        else:
            key_click(keycode=F2CODE, relay1=SHORTTIME * 8)  # 点f2取消

        time.sleep(SHORTTIME * 10)
        pos = win32api.GetCursorPos()
        pos = int(pos[0]) - fix[0], int(pos[1]) - fix[1]
        win32api.SetCursorPos(pos)  # 移动到商品页面购买键
        time.sleep(SHORTTIME)

        times -= 1


# 封装键盘输入
def key_click(keycode, relay1=SHORTTIME * 5, relay2=SHORTTIME,scanCode=None):
    sc=scanCode if scanCode!=None else 0
    time.sleep(relay1)
    win32api.keybd_event(keycode, sc, 0, 0)
    time.sleep(relay2)
    win32api.keybd_event(keycode, sc, win32con.KEYEVENTF_KEYUP, 0)


# 封装鼠标输入
def mouse_click(new_x=None, new_y=None, left=True, times=1):
    if new_x and new_y:
        point = (new_x, new_y)
        win32api.SetCursorPos(point)
    if left:
        down, up = win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP
    else:
        down, up = win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP
    while times:
        time.sleep(SHORTTIME)
        win32api.mouse_event(down, 0, 0, 0, 0)
        win32api.mouse_event(up, 0, 0, 0, 0)
        times -= 1


def getFormatedTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 默认进行10000次，遇到某些错误或者达成target会提前退出
def reJianDing(target, times=10e4, rows=None, cols=None, sh=1):
    ll.w(lc.zjdYugao.format(EQTYPES[sh], target, [ATTRS[i - 1] for i in rows], cols))

    # 当前鉴定次数,上次鉴定得分
    i, prePoint = 1, 0
    t1 = time.clock()
    template2 = cv2.cvtColor(ZJDSHOP, cv2.COLOR_RGB2BGR)
    pt = None
    top = shenhuaPoints[-1] if sh else puguanPoints[-1]

    # 鉴定得分的连续不变的次数 和其对应的程序退出次数
    errorTime2, quit2 = 0, 5

    while i <= times:
        # if lc.exitFlg: return

        mouse_click(left=False)
        time.sleep(SHORTTIME * 5)
        key_click(F1CODE)
        ll.i('{}第{}次鉴定开始'.format(getFormatedTime(), i))

        # 连续找不到鉴定所的次数 和其对应的程序退出次数
        # 未知bug可能连续无法找到鉴定所，连续3次时程序退出
        errorTime1, quit1 = 0, 3
        while 1:
            # if lc.exitFlg: return
            time.sleep(lc.ZJD_F1_WAITTIME)
            try:
                pt, point = lp.reJD(template2, pt, rows, cols, sh)
                break
            except AssertionError as e:
                errorTime1 += 1
                ll.e('reJianDing')
            if errorTime1 == 2:
                key_click(lc.F1CODE)
            if errorTime1 >= quit1:
                assert True, lc.error1msg.format(quit1)
                return
        level = round(point[0] / top, 2)
        # print(point , top)
        ll.i('鉴定结果为{}顶'.format(level))

        # if point[0]>=target*top
        # if point[0]>target*top-.1:
        if level > target - ZJDLOSS:
            t2 = round(time.clock() - t1, 2)
            ll.i('鉴定成功程序退出,耗时{}秒'.format(t2))
            return True
        i += 1

        # 未知bug往往导致鉴定结果连续不变，连续5次时退出程序
        if prePoint == point:
            ll.e("鉴定得分与上回相同，可能有bug出现")
            errorTime2 += 1
            if errorTime2 >= quit2 - 1:
                ll.e(lc.error2msg.format(quit2))
                return
        if prePoint != point:
            errorTime2 = 0
        prePoint, level = point, 0
        # print(errorTime2,prePoint,point)
    return True



def buy_tiqu_hebingall(itemcount,fix1=lc.FIX1):
    #购买
    buy(fix=fix1, times=itemcount)

    #移动到提取页面第一个商品
    fix2=lc.FIX2
    time.sleep(SHORTTIME * 5)
    pos = win32api.GetCursorPos()
    pos = int(pos[0]) + fix2[0], int(pos[1]) + fix2[1]
    win32api.SetCursorPos(pos)

    #开始提取(提取完后按esc关闭各页面)
    time.sleep(SHORTTIME * 5)
    takeItem(itemcount)

    #按i打开背包
    time.sleep(SHORTTIME * 10)
    key_click(lc.ICODE,scanCode=lc.ISCANCODE)

    #合并全背包的再鉴定
    time.sleep(SHORTTIME * 10)
    movZJDAll(threshold=lc.zjdThreshold)


def main():
    # t = threading.Thread(target=changeExitFlg, args=())
    # t.setDaemon(True)
    # t.start()
    while 1:
        # if lc.exitFlg: return
        inp = input(lc.mainmsg1)
        print('\t选择了{}:{}'.format(inp, lc.actions[inp]))
        if inp == '1':  # 买东西
            print(lc.waitmsg, lc.buymsg1)
            time.sleep(2)
            itemcount = int(input(lc.buymsg2))
            buy(times=itemcount)
        elif inp == '2':  # 提取商品
            print(lc.waitmsg, lc.tiqumsg1)
            time.sleep(2)

            itemcount = int(input(lc.tiqumsg2))
            takeItem(itemcount)
        elif inp == '3':  # 合并背包的再鉴定
            print(lc.waitmsg, lc.hebingmsg1)
            time.sleep(2)

            # 再鉴定的个数可能对图片识别造成影响,threshold取0.7效果不错
            # 找多了可适当提高threshold，找少了可适当降低threshold，如到降到0.63，或手动合并剩余的
            movZJD(threshold=lc.zjdThreshold)
        elif inp == '5':  # 合并所有背包的再鉴定
            print(lc.waitmsg, lc.hebingmsg1)
            time.sleep(2)
            movZJDAll(threshold=lc.zjdThreshold)
        elif inp == '6':  # 1+2+5
            print(lc.buy_tiqu_hebingall_msg1)
            print(lc.waitmsg, lc.buymsg1)
            time.sleep(2)

            fix1 = lc.FIX1
            itemcount = int(input(lc.buymsg2))
            buy_tiqu_hebingall(fix1, itemcount)
        elif inp == '4':  # 再鉴定
            inp_ = input(lc.zjdmsg2)
            if len(inp_) == 0:
                target = lc.zjdDict['target']
                rows = lc.zjdDict['rows']
                sh = lc.zjdDict['sh']
            else:
                inp_ = inp_.replace('，', ',')
                a, b, c = inp_.split(',')
                target = float(a)
                rows = [int(i) for i in b]
                print(rows)
                sh = int(c)

            cols = (1, 2, 3, 4, 5, 6, 7, 8)

            print(lc.waitmsg, lc.zjdmsg1)
            time.sleep(2)

            result = reJianDing(target=target, rows=rows, cols=cols, sh=sh)
            if not result:
                break
        elif inp == '8':  # 测试要检索图片的阈值
            print(lc.waitmsg, lc.yzmsg1)
            time.sleep(2)
            inp_ = input('请输入序号后回车,1:再鉴定,2:再鉴定商店,3:背包条\n')
            if inp_ == '1':
                template_, n, th = ZJD, lc.ZJDPATH, lc.zjdThreshold
            elif inp_ == '2':
                template_, n, th = ZJDSHOP, lc.ZJDSHOPPATH, lc.zjdShopThreshold
            elif inp_ == '3':
                template_, n, th = BAGS, lc.BAGSPATH, lc.bagsThreshold
            else:
                template_, n, th = None, None, None
            if n != None:
                t = cv2.cvtColor(template_, cv2.COLOR_RGB2BGR)
                lp.findTemplateInPic(t,threshold=th, istest=1, tname=n)
        elif inp == '9':  # 测量距离
            print(lc.waitmsg)
            time.sleep(2)

            measureDistance()
        else:
            print('退出main')
            break

def main2(inp,itemcount,target,sh,rows,yuzhi):
    if inp == '1':  # 买东西
        # print(lc.waitmsg, lc.buymsg1)
        time.sleep(2)
        # pass
        buy(times=itemcount)
    elif inp == '2':  # 提取商品
        # print(lc.waitmsg, lc.tiqumsg1)
        time.sleep(2)

        takeItem(itemcount)
    elif inp == '3':  # 合并背包的再鉴定
        # print(lc.waitmsg, lc.hebingmsg1)

        time.sleep(2)
        # 再鉴定的个数可能对图片识别造成影响,threshold取0.7效果不错
        # 找多了可适当提高threshold，找少了可适当降低threshold，如到降到0.63，或手动合并剩余的
        movZJD(threshold=lc.zjdThreshold)
    elif inp == '5':  # 合并所有背包的再鉴定
        # print(lc.waitmsg, lc.hebingmsg1)

        time.sleep(2)
        movZJDAll(threshold=lc.zjdThreshold)
    elif inp == '6':  # 1+2+5
        # print(lc.buy_tiqu_hebingall_msg1)
        # print(lc.waitmsg, lc.buymsg1)
        time.sleep(2)

        buy_tiqu_hebingall( itemcount)
    elif inp == '4':  # 再鉴定
        target = float(target)
        cols = (1, 2, 3, 4, 5, 6, 7, 8)

        # print(lc.waitmsg, lc.zjdmsg1)
        time.sleep(2)

        result = reJianDing(target=target, rows=rows, cols=cols, sh=sh)
    elif inp == '8':  # 测试要检索图片的阈值
        # print(lc.waitmsg, lc.yzmsg1)
        time.sleep(2)
        inp_ = yuzhi
        if inp_ == '1':
            template_, n, th = ZJD, lc.ZJDPATH, lc.zjdThreshold
        elif inp_ == '2':
            template_, n, th = ZJDSHOP, lc.ZJDSHOPPATH, lc.zjdShopThreshold
        elif inp_ == '3':
            template_, n, th = BAGS, lc.BAGSPATH, lc.bagsThreshold
        else:
            template_, n, th = None, None, None
        if n != None:
            t = cv2.cvtColor(template_, cv2.COLOR_RGB2BGR)
            x,_=lp.findTemplateInPic(t,threshold=th, istest=1, tname=n)
            # print(len(x))
    elif inp == '9':  # 测量距离
        # print(lc.waitmsg)
        time.sleep(2)
        measureDistance()



if __name__ == "__main__":
    main()
    # movZJDAll()
