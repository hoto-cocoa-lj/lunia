import math
import cv2 as cv


class Point(object):
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.F = 0
        self.G = 0
        self.H = 0


# 全局阈值
def threshold_demo(image):
    print(image.shape)
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  # 把输入图像灰度化
    # 直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    # print("threshold value %s" % ret)
    # cv.imshow("binary0", binary)
    return binary




def estimate_distance(from_point, target_point):
    f0,f1=from_point.position[0],from_point.position[1]
    t0,t1=target_point.position[0],target_point.position[0]
    # return math.sqrt(math.pow(t0 - f0, 2) + math.pow(t1 - f1, 2))
    return abs(t0 - f0)+abs(t1 - f1)


def is_same_node(point, target_point):
    if point.position[0] == target_point.position[0] and point.position[1] == target_point.position[1]:
        return True
    return False


def is_point_in_list(point, p_list):
    for p in p_list:
        if is_same_node(p, point):
            return True
    return False


def get_point_from_list(point, p_list):
    for p in p_list:
        if is_same_node(p, point):
            return p
    return None

def display_path_DIY(last_point,src,bi):
    point_path = []
    last_point = last_point.parent
    last_arrow=None
    fix1,fix2=1,2

    while 1:
        if last_point.parent==None:
            break
        tmp=last_point.parent
        arrow=tmp.position[0]-last_point.position[0],\
              tmp.position[1]-last_point.position[1]
        if arrow!=last_arrow:
            a,b=last_point.position
            if bi[a+fix1,b+fix1]==0:
                a,b=a-fix2,b-fix2
            elif bi[a-fix1,b+fix1]==0:
                a, b = a + fix2, b - fix2
            elif bi[a+fix1,b-fix1]==0:
                a, b = a - fix2, b + fix2
            elif bi[a-fix1,b-fix1]==0:
                a, b = a + fix2, b + fix2

            if len(point_path)==0:
                point_path.append((a, b))
            elif abs(point_path[-1][0]-a)<=2 and abs(point_path[-1][1]-b)<=2:
                point_path[-1]=(a,b)
            else:
                point_path.append((a, b))
        last_point = last_point.parent
        last_arrow=arrow
    point_path.reverse()
    return point_path


def display_path(last_point,src,bi):
    point_path = [last_point]
    last_point = last_point.parent
    while last_point is not None:
        point_path.append(last_point)
        last_point = last_point.parent

    point_path.reverse()
    print(len(point_path))
    # path_str = ''
    # for p in point_path:
    #     path_str += '[' + str(p.position[0]) + ',' + str(p.position[1]) + ']-->'
    # print(path_str)

    # image = src
    # for point in point_path:
    #     cv.circle(image, (point.position[1], point.position[0]), 1, (0, 0, 255), 1)
    # image = cv.resize(image, (bi.shape[1] * 4, bi.shape[0] * 4))
    # cv.imshow("final", image)


def filter_not_reachables_DIY(map, points):
    new_points = []
    fix=1
    for point in points:
        x,y=point.position[0],point.position[1]
        if map[x+ fix][y] == 255\
        and map[x][y-fix] == 255 \
        and map[x-fix][y] == 255\
        and map[x][y + fix] == 255:
            new_points.append(point)

    return new_points

def filter_not_reachables(map, points):
    new_points = []

    for point in points:
        if map[point.position[0]][point.position[1]] == 255:
            new_points.append(point)

    return new_points


def get_periphery_points(map, point,addX=0):
    points = []

    x = point.position[0]
    y = point.position[1]


    points.append(Point([x, y - 1], None))
    points.append(Point([x - 1, y], None))
    points.append(Point([x + 1, y], None))
    points.append(Point([x, y + 1], None))

    if addX:
        points.append(Point([x - 1, y - 1], None))
        points.append(Point([x + 1, y - 1], None))
        points.append(Point([x - 1, y + 1], None))
        points.append(Point([x + 1, y + 1], None))

    valid_points = []

    for p in points:
        if 0 <= p.position[0] < map.shape[0] and 0 <= p.position[1] < map.shape[1]:
            valid_points.append(p)

    return valid_points


def pick_one_min_F_point(p_list):
    if len(p_list) == 0:
        return None

    if len(p_list) == 1:
        return p_list[0]

    min_F = p_list[0].F
    min_idx = 0

    for idx, p in enumerate(p_list[1:]):
        if p.F < min_F:
            min_F = p.F
            min_idx = idx + 1

    return p_list[min_idx]


def filter_ignored(points):
    new_points = []

    if len(points) <= 0:
        return new_points

    for p in points:
        if p.ignore:
            continue
        new_points.append(p)

    return new_points


def a_star(map,src,target_point=None,from_point=None):
    width, height = map.shape

    if target_point == None:
        target_point = Point([width - 1, height - 1], None)
    if from_point==None:
        from_point = Point([0, 0], None)

    from_point.G = 0
    from_point.H = estimate_distance(from_point, target_point)
    from_point.F = from_point.G + from_point.H

    open_list = []
    close_list = []
    open_list.append(from_point)

    while len(open_list) > 0:
        cur_point = pick_one_min_F_point(open_list)
        if cur_point is None:
            raise ValueError('无法找到可达路径')

        points = get_periphery_points(map, cur_point)
        # points = filter_not_reachables_DIY(map, points)
        points = filter_not_reachables(map, points)

        for point in points:
            if is_point_in_list(point, open_list):
                point.new_added = False
                point.ignore = False
                p = get_point_from_list(point, open_list)
                point.parent = p.parent
                point.F = p.F
                point.G = p.G
                point.H = p.H
            elif is_point_in_list(point, close_list):
                point.new_added = False
                point.ignore = True
                p = get_point_from_list(point, close_list)
                point.parent = p.parent
                point.F = p.F
                point.G = p.G
                point.H = p.H
            else:
                point.new_added = True
                point.ignore = False
                open_list.append(point)

        points = filter_ignored(points)

        for point in points:
            if point.new_added:
                point.parent = cur_point
                # 计算FGH
                point.G = cur_point.G + 1
                point.H = estimate_distance(point, target_point)
                point.F = point.G + point.H
            else:
                # 计算FGH
                old_f = point.G + point.H
                new_f = cur_point.G + 1 + point.H

                # 比较新的和老的F值哪个大
                if new_f < old_f:
                    # 覆盖新的FGH/PARENT
                    point.parent = cur_point
                    point.G = cur_point.G + 1
                    point.F = point.G + point.H

        for point in points:
            if is_same_node(point, target_point):
                return display_path_DIY(point,src,map)


        open_list.remove(cur_point)
        close_list.append(cur_point)

def main(fp,from_pos,target_pos):
    # src = cv.imread('E:\picmodify\lunia\pic\capture/1.jpg')
    src = cv.imread(fp)
    # src = cv.imread('E:\picmodify\lunia\pic\capture/1.jpg',flags=0)
    if 1:
        bi = threshold_demo(src)
    else:
        bi = src
    from_point = Point(from_pos, None)
    target_point = Point(target_pos, None)

    return a_star(bi,src, target_point, from_point)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

if __name__=='__main__':
    fp='E:\picmodify\lunia\pic\capture/1.jpg'
    from_pos=[60, 122]
    target_pos=[70, 50]
    main(fp,from_pos,target_pos)
