import win32api, win32con, time, cv2,win32gui,os,sys,numpy as np
from PIL import Image, ImageGrab

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import lunia.pictool as lp, lunia.constant as lc,lunia.luniatool as lt,lunia.numberpictool as ln

class AccessoryTool:
    windowTitle=lc.gameWindowTitle
    prepareOffset=(725,365)
    inputboxOffset=(400,375)
    inputokOffset=(411,416)
    loseOffset=(83,574)
    getoutOffset=(503,614)
    codeOffset1=(390,320)
    codeOffset2=(420,335)
    wds,wdposes=[],[]
    npt=ln.NumberPicTool()
    #游戏要等130s才能退出，加载有时要半分钟以上，姑且给50s
    wait1,wait2=130,40
    #胜利等到30s
    wait3,wait4=30,7
    runTimes=None
    teamPersons=None
    wait5=1
    # state=win32con.SW_SHOWMINNOACTIVE

    def findLuniaWindows(self,x,mouse):
        if win32gui.GetWindowText(x)==self.windowTitle:
            self.wds.append(x)
            self.wdposes.append(win32gui.GetWindowRect(x))
        self.teamPersons=int(len(self.wds)/2)

    def calculatePos(self,i,offset):
        return self.wdposes[i][0] + offset[0],  self.wdposes[i][1] + offset[1]

    # 第i窗口点击准备
    def prepare(self,i):
        #把窗口移动到最前面
        time.sleep(self.wait5)
        win32gui.SetForegroundWindow(self.wds[i])
        time.sleep(1)

        pos = self.calculatePos(i, self.prepareOffset)
        time.sleep(self.wait5)
        win32api.SetCursorPos(pos)
        time.sleep(self.wait5)
        lt.mouse_click()

        time.sleep(self.wait5)
        pos = self.calculatePos(i, self.inputboxOffset)
        win32api.SetCursorPos(pos)
        time.sleep(self.wait5)
        lt.mouse_click()

        code=self.getCode(i)
        print('\t第{}个窗口code是{}'.format(i,code))

        for j in code:
            lt.key_click(keycode=48+int(j))

        time.sleep(self.wait5)
        pos = self.calculatePos(i, self.inputokOffset)
        win32api.SetCursorPos(pos)
        time.sleep(self.wait5)
        lt.mouse_click()

        #是否需要最小化
        # time.sleep(self.wait5)
        # win32gui.ShowWindow(self.wds[i], self.state)

    def startGame(self,i=0):
        #把窗口移动到最前面
        time.sleep(self.wait5)
        win32gui.SetForegroundWindow(self.wds[i])
        time.sleep(1)

        pos = self.calculatePos(i, self.prepareOffset)
        time.sleep(self.wait5)
        win32api.SetCursorPos(pos)
        time.sleep(self.wait5)
        lt.mouse_click()

        # 是否需要最小化
        # time.sleep(self.wait5)
        # win32gui.ShowWindow(self.wds[i], self.state)

    # 第i窗口认输
    def loseGame(self,i):
        time.sleep(self.wait5)
        win32gui.SetForegroundWindow(self.wds[i])
        time.sleep(1)

        time.sleep(self.wait5)
        lt.key_click(keycode=lc.ESCCODE,scanCode=lc.ESCSCANCODE)

        pos = self.calculatePos(i, self.loseOffset)
        time.sleep(self.wait5)
        win32api.SetCursorPos(pos)
        time.sleep(self.wait5)
        lt.mouse_click()

        time.sleep(self.wait5)
        lt.key_click(keycode=lc.F1CODE)

    # 第i窗口截图
    def captureWindow(self,i,offset1,offset2,doActive=False):
        if doActive:
            time.sleep(self.wait5)
            win32gui.SetForegroundWindow(self.wds[i])
            time.sleep(1)
        return self.capture(*self.calculatePos(i,offset1),
                            *self.calculatePos(i,offset2))

    def capture(self,x1, y1, x2, y2):
        img = ImageGrab.grab((x1, y1, x2, y2))
        # img = binaryPic(img)
        # cv2.imwrite(r'D:\360down\2.png',img)
        # img.save(r'D:\360down\2.png')
        return img

    #读取第i个窗口的验证码
    def getCode(self,i):
        # img1=Image.open(r"D:\360down\1.png")
        # text = pytesseract.image_to_string(img1)
        img= self.captureWindow(i,self.codeOffset1,self.codeOffset2)
        img=np.asarray(img)
        code=self.npt.getCode(img)
        return code

    def sortWindows(self):
        #to do:这里要测试顺序是否正确，貌似对了
        self.wds=[x for y, x in sorted(zip(self.wdposes,self.wds),key=lambda x:x[0][0])]
        self.wdposes=sorted(self.wdposes,key=lambda x:x[0])
        print('窗口句柄是{}'.format(self.wds))
        print('窗口坐标是{}'.format(self.wdposes))

    def __init__(self,runTimes=70):
        self.runTimes=runTimes
        win32gui.EnumWindows(self.findLuniaWindows, 0)
        self.sortWindows()

    def progress(self,reverse=True):
        for i in range(1,len(self.wds)):
            time.sleep(.5)
            self.prepare(i)

        time.sleep(.5)
        self.startGame()

        #听说等130s即可，加载地图也要时间
        time.sleep(self.wait1+self.wait2)
        if reverse:
            from_,to_=self.teamPersons,len(self.wds)
        else:
            from_,to_=0,self.teamPersons
        for i in range(from_,to_):
            time.sleep(.5)
            self.loseGame(i)

    def main(self,reverse=True,runTimes=None):
        i=0
        while i<runTimes:
            i+=1
            print('{}\t第{}/{}轮{}开始'.format(lt.getFormatedTime(),i,runTimes,reverse))
            self.progress(reverse)
            time.sleep(self.wait3+self.wait4*self.teamPersons)




if __name__ == "__main__":
    at=AccessoryTool()
    at.main(reverse=1,runTimes=0)
    at.main(reverse=0,runTimes=12)

