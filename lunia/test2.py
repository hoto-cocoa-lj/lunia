import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2,lunia.constant as lc,lunia.accessorytool as la
import numpy as np,lunia.pictool as lp

fp = 'E:\picmodify\lunia\pic\capture/1.bmp'
img=cv2.imread(fp)
a=lp.getPosByColorGray(img,255)
print(a)
b=np.array(a)
c=np.argmin(a,axis=0)
print(b[c[0]])
print(c)
print(b)
print(np.min(a,0))
img[61:64,39:55]=255
img[68:71,44:80]=255

cv2.imshow('1',img);cv2.waitKey(0)
cv2.imwrite('E:\picmodify\lunia\pic\capture/2.jpg',img)
