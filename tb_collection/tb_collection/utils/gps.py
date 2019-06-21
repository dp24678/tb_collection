# _*_coding:utf-8 _*_
#@Time    :2019/6/21 17:47
#@Author  :Dapan
#@Email : 248312738@qq.com

import math
import random


def generate_random_gps(base_log=120.7, base_lat=30, radius=1000000):
    """
    生成随机经纬度  base_log=120.7, base_lat=30, radius=1000000：国内经纬度
    :param base_log:经度基准点，
    :param base_lat:维度基准点，
    :param radius:距离基准点的半径
    :return:生成的经纬度数据
    """
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    # 这里是想保留14位小数
    loga = '%.14f' % longitude
    lata = '%.14f' % latitude

    print('经度: %s' % loga)  # 经度
    print('纬度: %s' % lata)  # 纬度
    return loga, lata

if __name__ == '__main__':
    # generate_random_gps(base_log=120.7, base_lat=30, radius=1000000)
    generate_random_gps()