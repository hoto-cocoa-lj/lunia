import cv2
import numpy as np

class NumberPicTool:
    templatePadding=0
    threshold_=130
    numberPics = []

    def __init__(self):
        for i in range(10):
            pic=cv2.imread(r"./pic/numbers/{}.png".format(i),flags=0)
            self.numberPics.append(pic)


    def getCode(self,img_=None):
        # img_ = cv2.imread(r"D:\360down\2.png")
        # img_ = cv2.resize(img_, None, None, fx=3, fy=3)

        img = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)

        _, img = cv2.threshold(img, self.threshold_, 255, cv2.THRESH_BINARY)
        # cv2.imwrite(r"D:\360down\3.png",img)
        cnts, _ = cv2.findContours(img,
                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # img_1=img_.copy()
        # cv2.drawContours(img_1, cnts, -1, (255, 0, 0), 1)
        # cv2.imwrite(r"D:\360down\4.png", img_1)

        # img_2 = img_.copy()
        rects=[cv2.boundingRect(c) for c in cnts]
        rects=sorted(rects,key=lambda x:x[0])
        # for r in rects:
        #     cv2.rectangle(img_2, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]),(0,255,0),1)
        # cv2.imwrite(r"D:\360down\5.png", img_2)
        nums=[]
        for i,r in enumerate(rects):
            im=img[r[1]-self.templatePadding:r[1]+r[3]+self.templatePadding,
                    r[0]-self.templatePadding:r[0]+r[2]+self.templatePadding]
            # cv2.imwrite(r"D:\360down\{}_{}.png".format(0,i), im)

            scores=[]
            for j,p in enumerate(self.numberPics):
                if im.shape[-1]==2:
                    # img_ = cv2.resize(img_, None, None, fx=3, fy=3)
                    im=cv2.resize(im,(4,9),None,fx=None,fy=None)
                result=cv2.matchTemplate(im,p,cv2.TM_CCOEFF)
                scores.append(result)
            nums.append(str(np.argmax(scores)))
        return nums

def main():
    NumberPicTool().getCode()


if __name__ == "__main__":
    main()
