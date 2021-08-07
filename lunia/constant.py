from collections import defaultdict

#再鉴定参数
# target:几倍顶,rows:需要哪些属性
#攻击力1,力量2,敏捷3,智能4,健康5,防御力6,生命力7,魔力8
#sh:是否为神话装备(是:1,否:0)
#如鉴定力量智能3顶的神话装备{'target':3,'rows':(2, 4),'sh':1}
#如鉴定力量敏捷1.5顶的普关装备{'target':1.5,'rows':(2, 3),'sh':0}
zjdDict={'target':1.5,'rows':(2, 3),'sh':1}

#图片阈值设定
# zjdThreshold=0.65
# shanguangbaoshiThreshold=0.49
zjdThreshold=0.65
zjdShopThreshold=0.9
bagsThreshold=0.5

# 再鉴定的项目的区域大小(w1*h)是88*15
# 再鉴定的数值的区域大小(w2*h)是50*15
# 此数据对鉴定数据的识别有一定影响，越精确越好
w1,w2,h=88,50,15

#FIX1:商品列表里再鉴定的购买按钮a 到弹出窗的购买按钮b 的像素距离
# a在b右边时第1个值取负数,a在b下边时第2个值取负数。可能需要修改
# FIX1 = (-79, -34)
FIX1 = (90, 350)

#FIX2:
FIX2 = (-44, 44)


################以上可修改##################################
###########################################################
###########################################################
###########################################################
###########################################################
###########################################################
###########################################################
###############以下不用修改#################################


ZJD_F1_WAITTIME=3
PrtScr_WAITTIME=1

#3鉴数据来自群里0595BE-0A9AC3
#颜色阈值，0鉴定是20-37，1鉴是102-113，2鉴是155-162，3鉴是190-195
#0鉴定是20-37指暗色列如力量约20，亮色列如敏捷约37，误差5以内
#todo COLOR_LEVEL_3和COLOR_LEVEL_4还没定，估计没问题，
#而且COLOR_LEVEL_4作用很小
COLOR_LEVEL_1=70
COLOR_LEVEL_2=135
COLOR_LEVEL_3=175
COLOR_LEVEL_4=256

#生成的图片的文件名
RESULTJPG='result.jpg'
RESULT2JPG='result2.jpg'

#查找用的图片的文件名或路径
PICDIR='./pic/'
CAPTUREDIR='./pic/capture/'
SCREENJPG='screen.jpg'
ZJDPATH='zjd.png'
ZJDSHOPPATH='zjdshop.png'
BAGSPATH='bags.png'

#等待时间
SHORTTIME=.1

#再鉴定的属性类型
ATTRS=['攻击力','力量','敏捷','智能','健康','防御力','生命力','魔力']
ATTRSSTR=''
for i in range(len(ATTRS)):
    ATTRSSTR+='{}:{},'.format(ATTRS[i],i+1)
ATTRSSTR='{'+ATTRSSTR[:-1]+'}'

#points分别取自魔族衣服和火花武器,少量修改
shenhuaPoints=[-4,-2,1,2,4,6,12,24]
puguanPoints=[-3,-2,2,6,12,18,36,54]

# python小数计算不精确,
# 用>target-ZJDLOSS代替>=target来判断是否达成目标
ZJDLOSS=.02

#一些键码
F1CODE=112
F2CODE=113
ESCCODE=27
ESCSCANCODE=1
ICODE=27
ISCANCODE=23

EQTYPES=['普关','神话']

exitFlg=False

measureDistanceStr1='请将光标移动到起点,之后按回车'
measureDistanceStr2='移动到终点,之后按回车'
zjdYugao='{}装备,鉴定目标是{}顶,属性范围是{},允许的鉴定级别是{}'
error1msg='连续{}次无法找到鉴定所,程序退出'
error2msg='鉴定得分连续{}次未发生改变,程序退出'

actions=defaultdict(str)
actions['1']='购买'
actions['2']='提取'
actions['3']='合并'
actions['4']='再鉴定'
actions['5']='多背包合并'
actions['6']='购买+提取+多背包合并'
actions['8']='测试阈值'
actions['9']='测量距离'
mainmsg1=''
for x in actions:
    mainmsg1+='\t'+x+":"+actions[x]+"\n"
mainmsg1='请输入对应的数字:\n{}\t其他:退出\n'.format(mainmsg1)

waitmsg='2秒后程序进行处理,'
buymsg1='请将光标移动到商品的购买按钮上'
buymsg2='请输入购买的次数,每次只能买一个\n'

tiqumsg1='请将光标移动到要提取的商品上'
tiqumsg2='请输入提取的次数,每次只能提取一个\n'

hebingmsg1='请保证背包窗口能看见'

measuremsg1='此功能需要在Python Shell窗口操作，不建议使用。请使用微信qq等工具测量'

buy_tiqu_hebingall_msg1='！！！请确保已正确设置constant.py里的FIX2，否则可能出现无法预料的错误！！！\n'

zjdmsg1='请右键再鉴定,放上要鉴定的装备,将光标移动到再鉴定上'
zjdmsg2='\n\n请输入目标值,需要属性和是否为神话装备(是:1,否:0),用逗号隔开,\n属性有{}\n' \
        '如鉴定力量智能3顶的神话装备时输入3,24,1后按回车\n' \
        '如鉴定力量敏捷1.5顶的普关装备时输入1.5,23,0后按回车\n' \
        '建议修改constant.py后，直接按回车运行\n'.format(ATTRSSTR)

yzmsg1='请保证要测试的图片在屏幕上可见，如果程序卡5秒以上请点击游戏窗口或关闭程序'

logFile='all.log'

windowName="HOTO COCOA"

gameWindowTitle='[#] Lunia [#]'

smpfix=3
SMP=[[631+smpfix, 52+smpfix],
     [798-smpfix, 199-smpfix]]
# smallMapPos=[[SMP[0][0],SMP[0][1]+20],[SMP[1][0], SMP[1][1]-20]]
smallMapPos=SMP
smallMapThreshold=70

upKey=4*16+8
downKey=5*16
leftKey=4*16+11
rightKey=4*16+13
leftDownKey=4*16+15
arrowMap={upKey:'up',downKey:'down',leftKey:'left',rightKey:'right'}
#mo1 chushi 61,41,(69, 57)

#(63,55),(70,55)
#(70,73),(76,73)