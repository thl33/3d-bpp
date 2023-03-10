import math
import time
import random
import numpy as np
import pandas as pd
import concurrent.futures
from model import PlacementProcedure, generateInputs, BRKGA
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from plot import plot_3D


"""
inputs 参数说明：
p, q, r 为货物的长、宽、高的尺寸
L, W, H 为集装箱（货车）的长、宽、高的尺寸
为了具有一般性，在这里我们定义货物的尺寸都小于集装箱的尺寸
"""

# # 3种箱子
# # E1-1
l1, w1, h1, n1 = 108, 76, 30, 40
l2, w2, h2, n2 = 110, 43, 25, 33
l3, w3, h3, n3 = 92, 81, 55, 39
# # E1-2
# l1, w1, h1, n1 = 91, 54, 45, 32
# l2, w2, h2, n2 = 105, 77, 72, 24
# l3, w3, h3, n3 = 79, 78, 48, 30
# # E1-3
# l1, w1, h1, n1 = 91, 54, 45, 32
# l2, w2, h2, n2 = 105, 77, 72, 24
# l3, w3, h3, n3 = 79, 78, 48, 30
# # E1-4
# l1, w1, h1, n1 = 60, 40, 32, 64
# l2, w2, h2, n2 = 98, 75, 55, 40
# l3, w3, h3, n3 = 60, 59, 39, 64
# # E1-5
# l1, w1, h1, n1 = 78, 37, 27, 63
# l2, w2, h2, n2 = 89, 70, 25, 52
# l3, w3, h3, n3 = 90, 84, 41, 55
# # 5种箱子
# # E2-1
# l1, w1, h1, n1 = 108, 76, 30, 24
# l2, w2, h2, n2 = 110, 43, 25, 7
# l3, w3, h3, n3 = 92, 81, 55, 22
# l4, w4, h4, n4 = 81, 33, 28, 13
# l5, w5, h5, n5 = 120, 99, 73, 15
# # E2-2
# l1, w1, h1, n1 = 49, 25, 21, 22
# l2, w2, h2, n2 = 60, 51, 41, 22
# l3, w3, h3, n3 = 103, 76, 64, 28
# l4, w4, h4, n4 = 95, 70, 62, 25
# l5, w5, h5, n5 = 111, 49, 26, 17
# # E2-3
# l1, w1, h1, n1 = 88, 54, 39, 25
# l2, w2, h2, n2 = 94, 54, 36, 27
# l3, w3, h3, n3 = 87, 77, 43, 21
# l4, w4, h4, n4 = 100, 80, 72, 20
# l5, w5, h5, n5 = 83, 40, 36, 24
# # E2-4
# l1, w1, h1, n1 = 90, 70, 63, 16
# l2, w2, h2, n2 = 84, 78, 28, 28
# l3, w3, h3, n3 = 94, 85, 39, 20
# l4, w4, h4, n4 = 80, 76, 54, 23
# l5, w5, h5, n5 = 69, 50, 45, 31
# # E2-5
# l1, w1, h1, n1 = 74, 63, 61, 22
# l2, w2, h2, n2 = 71, 60, 25, 12
# l3, w3, h3, n3 = 106, 80, 39, 20
# l4, w4, h4, n4 = 109, 76, 42, 24
# l5, w5, h5, n5 = 118, 56, 22, 11
# # 8种箱子
# # E3-1
# l1, w1, h1, n1 = 108, 76, 30, 24
# l2, w2, h2, n2 = 110, 43, 25, 9
# l3, w3, h3, n3 = 92, 81, 55, 8
# l4, w4, h4, n4 = 81, 33, 28, 11
# l5, w5, h5, n5 = 120, 99, 73, 11
# l6, w6, h6, n6 = 111, 70, 48, 10
# l7, w7, h7, n7 = 98, 72, 46, 12
# l8, w8, h8, n8 = 95, 66, 31, 9
# # E3-2
# l1, w1, h1, n1 = 97, 81, 27, 10
# l2, w2, h2, n2 = 102, 78, 39, 20
# l3, w3, h3, n3 = 113, 46, 36, 18
# l4, w4, h4, n4 = 66, 50, 42, 21
# l5, w5, h5, n5 = 101, 30, 26, 16
# l6, w6, h6, n6 = 100, 56, 35, 17
# l7, w7, h7, n7 = 91, 50, 40, 22
# l8, w8, h8, n8 = 106, 61, 56, 19
# # E3-3
# l1, w1, h1, n1 = 88, 54, 39, 16
# l2, w2, h2, n2 = 94, 54, 36, 14
# l3, w3, h3, n3 = 87, 77, 43, 20
# l4, w4, h4, n4 = 100, 80, 72, 16
# l5, w5, h5, n5 = 83, 40, 36, 6
# l6, w6, h6, n6 = 91, 54, 22, 15
# l7, w7, h7, n7 = 109, 58, 54, 17
# l8, w8, h8, n8 = 94, 55, 30, 9
# # E3-4
# l1, w1, h1, n1 = 49, 25, 21, 16
# l2, w2, h2, n2 = 60, 51, 41, 8
# l3, w3, h3, n3 = 103, 74, 64, 16
# l4, w4, h4, n4 = 95, 70, 62, 18
# l5, w5, h5, n5 = 111, 49, 26, 18
# l6, w6, h6, n6 = 85, 84, 72, 16
# l7, w7, h7, n7 = 48, 36, 31, 17
# l8, w8, h8, n8 = 86, 76, 38, 6
# # E3-5
# l1, w1, h1, n1 = 113, 92, 33, 23
# l2, w2, h2, n2 = 52, 37, 28, 22
# l3, w3, h3, n3 = 57, 33, 29, 26
# l4, w4, h4, n4 = 99, 37, 30, 17
# l5, w5, h5, n5 = 92, 64, 33, 23
# l6, w6, h6, n6 = 119, 59, 39, 26
# l7, w7, h7, n7 = 54, 52, 49, 18
# l8, w8, h8, n8 = 75, 45, 35, 30
# # E4-1
# l1, w1, h1, n1 = 49, 25, 21, 13
# l2, w2, h2, n2 = 60, 51, 41, 9
# l3, w3, h3, n3 = 103, 76, 64, 11
# l4, w4, h4, n4 = 95, 70, 62, 14
# l5, w5, h5, n5 = 111, 49, 26, 13
# l6, w6, h6, n6 = 85, 84, 72, 16
# l7, w7, h7, n7 = 48, 36, 31, 12
# l8, w8, h8, n8 = 86, 76, 38, 11
# l9, w9, h9, n9 = 71, 48, 47, 16
# l10, w10, h10, n10 = 90, 43, 33, 8
# # E4-2
# l1, w1, h1, n1 = 97,81, 27, 8
# l2, w2, h2, n2 = 102, 78, 39, 16
# l3, w3, h3, n3 = 113, 46, 36, 12
# l4, w4, h4, n4 = 60, 59, 42, 12
# l5, w5, h5, n5 = 101, 30, 26, 18
# l6, w6, h6, n6 = 100, 56, 35, 13
# l7, w7, h7, n7 = 91, 50, 40, 14
# l8, w8, h8, n8 = 106, 61, 56, 17
# l9, w9, h9, n9 = 103, 63, 58, 12
# l10, w10, h10, n10 = 75, 57, 41, 13
# # E4-3
# l1, w1, h1, n1 = 86, 84, 45, 18
# l2, w2, h2, n2 = 81, 45, 34, 19
# l3, w3, h3, n3 = 70, 54, 37, 13
# l4, w4, h4, n4 = 71, 61, 52, 16
# l5, w5, h5, n5 = 78, 73, 40, 10
# l6, w6, h6, n6 = 69, 63, 46, 13
# l7, w7, h7, n7 = 73, 67, 56, 10
# l8, w8, h8, n8 = 75, 75, 36, 8
# l9, w9, h9, n9 = 94, 88, 50, 12
# l10, w10, h10, n10 = 65, 51, 50, 13
# # E4-4
# l1, w1, h1, n1 = 113, 92, 33, 15
# l2, w2, h2, n2 = 52, 37, 28, 17
# l3, w3, h3, n3 = 57, 33, 29, 17
# l4, w4, h4, n4 = 99, 37, 30, 19
# l5, w5, h5, n5 = 92, 64, 33, 13
# l6, w6, h6, n6 = 119, 59, 39, 19
# l7, w7, h7, n7 = 54, 52, 49, 13
# l8, w8, h8, n8 = 75, 45, 35, 21
# l9, w9, h9, n9 = 79, 68, 44, 13
# l10, w10, h10, n10 = 116, 49, 47, 22
# # E4-5
# l1, w1, h1, n1 = 118, 79, 51, 16
# l2, w2, h2, n2 = 86, 32, 31, 8
# l3, w3, h3, n3 = 64, 58, 52, 14
# l4, w4, h4, n4 = 42, 42, 32, 14
# l5, w5, h5, n5 = 64, 55, 43, 16
# l6, w6, h6, n6 = 84, 70, 35, 10
# l7, w7, h7, n7 = 76, 57, 36, 14
# l8, w8, h8, n8 = 95, 60, 55, 14
# l9, w9, h9, n9 = 80, 66, 52, 14
# l10, w10, h10, n10 = 109, 73, 23, 18
# # E5-1
# l1, w1, h1, n1 = 98, 73, 44, 6
# l2, w2, h2, n2 = 60, 60, 38, 7
# l3, w3, h3, n3 = 105, 73, 60, 10
# l4, w4, h4, n4 = 90, 77, 52, 3
# l5, w5, h5, n5 = 66, 58, 24, 5
# l6, w6, h6, n6 = 106, 76, 55, 10
# l7, w7, h7, n7 = 55, 44, 36, 12
# l8, w8, h8, n8 = 82, 58, 23, 7
# l9, w9, h9, n9 = 74, 61, 58, 6
# l10, w10, h10, n10 = 81, 39, 24, 8
# l11, w11, h11, n11 = 71, 65, 39, 11
# l12, w12, h12, n12 = 105, 97, 47, 4
# l13, w13, h13, n13 = 114, 97, 69, 5
# l14, w14, h14, n14 = 103, 78, 55, 6
# l15, w15, h15, n15 = 93, 66, 55, 6
# # E5-2
# l1, w1, h1, n1 = 108, 76, 30, 12
# l2, w2, h2, n2 = 110, 43, 25, 12
# l3, w3, h3, n3 = 92, 81, 55, 6
# l4, w4, h4, n4 = 81, 33, 28, 9
# l5, w5, h5, n5 = 120, 99, 73, 5
# l6, w6, h6, n6 = 111, 70, 48, 12
# l7, w7, h7, n7 = 98, 72, 46, 9
# l8, w8, h8, n8 = 95, 66, 31, 10
# l9, w9, h9, n9 = 85, 84, 30, 8
# l10, w10, h10, n10 = 71, 32, 25, 3
# l11, w11, h11, n11 = 36, 34, 25, 10
# l12, w12, h12, n12 = 97, 67, 62, 7
# l13, w13, h13, n13 = 33, 25, 23, 7
# l14, w14, h14, n14 = 95, 27, 26, 10
# l15, w15, h15, n15 = 94, 81, 44, 9
# # E5-3
# l1, w1, h1, n1 = 49, 25, 21, 13
# l2, w2, h2, n2 = 60, 51, 41, 9
# l3, w3, h3, n3 = 103, 76, 64, 8
# l4, w4, h4, n4 = 95, 70, 62, 6
# l5, w5, h5, n5 = 111, 49, 26, 10
# l6, w6, h6, n6 = 74, 42, 40, 4
# l7, w7, h7, n7 = 85, 84, 72, 10
# l8, w8, h8, n8 = 48, 36, 31, 10
# l9, w9, h9, n9 = 86, 76, 38, 12
# l10, w10, h10, n10 = 71, 48, 47, 14
# l11, w11, h11, n11 = 90, 43, 33, 9
# l12, w12, h12, n12 = 98, 52, 44, 9
# l13, w13, h13, n13 = 73, 37, 23, 10
# l14, w14, h14, n14 = 61, 48, 39, 14
# l15, w15, h15, n15 = 75, 75, 63, 11
# # E5-4
# l1, w1, h1, n1 = 97, 81, 27, 6
# l2, w2, h2, n2 = 102, 78, 39, 6
# l3, w3, h3, n3 = 113, 46, 36, 15
# l4, w4, h4, n4 = 66, 50, 42, 8
# l5, w5, h5, n5 = 101, 30, 26, 6
# l6, w6, h6, n6 = 100, 56, 35, 7
# l7, w7, h7, n7 = 91, 50, 40, 12
# l8, w8, h8, n8 = 106, 61, 56, 10
# l9, w9, h9, n9 = 103, 63, 58, 8
# l10, w10, h10, n10 = 75, 57, 41, 11
# l11, w11, h11, n11 = 71, 68, 64, 6
# l12, w12, h12, n12 = 85, 67, 39, 14
# l13, w13, h13, n13 = 97, 63, 56, 9
# l14, w14, h14, n14 = 61, 48, 30, 11
# l15, w15, h15, n15 = 80, 54, 35, 9
# # E5-5
# l1, w1, h1, n1 = 113, 92, 33, 8
# l2, w2, h2, n2 = 52, 37, 28, 12
# l3, w3, h3, n3 = 57, 33, 29, 5
# l4, w4, h4, n4 = 99, 37, 30, 12
# l5, w5, h5, n5 = 92, 64, 33, 9
# l6, w6, h6, n6 = 119, 59, 39, 12
# l7, w7, h7, n7 = 54, 52, 49, 8
# l8, w8, h8, n8 = 75, 45, 35, 6
# l9, w9, h9, n9 = 79, 68, 44, 12
# l10, w10, h10, n10 = 116, 49, 47, 9
# l11, w11, h11, n11 = 83, 44, 23, 11
# l12, w12, h12, n12 = 98, 96, 56, 10
# l13, w13, h13, n13 = 78, 72, 57, 8
# l14, w14, h14, n14 = 98, 88, 47, 9
# l15, w15, h15, n15 = 41, 33, 31, 13

L_box , W_box, H_box = 587, 233, 220
box_max = 2
inputs = {
    # # 3种箱子
    'p': [l1] * n1 + [l2] * n2 + [l3] * n3,
    'q': [w1] * n1 + [w2] * n2 + [w3] * n3,
    'r': [h1] * n1 + [h2] * n2 + [h3] * n3,
    # # 5种箱子
    # 'p': [l1] * n1 + [l2] * n2 + [l3] * n3 + [l4] * n4 + [l5] * n5,
    # 'q': [w1] * n1 + [w2] * n2 + [w3] * n3 + [w4] * n4 + [w5] * n5,
    # 'r': [h1] * n1 + [h2] * n2 + [h3] * n3 + [h4] * n4 + [h5] * n5,
    # # 8种箱子
    # 'p': [l1] * n1 + [l2] * n2 + [l3] * n3 + [l4] * n4 + [l5] * n5 + [l6] * n6 + [l7] * n7 + [l8] * n8,
    # 'q': [w1] * n1 + [w2] * n2 + [w3] * n3 + [w4] * n4 + [w5] * n5 + [w6] * n6 + [w7] * n7 + [w8] * n8,
    # 'r': [h1] * n1 + [h2] * n2 + [h3] * n3 + [h4] * n4 + [h5] * n5 + [h6] * n6 + [h7] * n7 + [h8] * n8,
    # # 10种箱子
    # 'p': [l1] * n1 + [l2] * n2 + [l3] * n3 + [l4] * n4 + [l5] * n5 + [l6] * n6 + [l7] * n7 + [l8] * n8 + [l9] * n9 + [l10] * n10,
    # 'q': [w1] * n1 + [w2] * n2 + [w3] * n3 + [w4] * n4 + [w5] * n5 + [w6] * n6 + [w7] * n7 + [w8] * n8 + [w9] * n9 + [w10] * n10,
    # 'r': [h1] * n1 + [h2] * n2 + [h3] * n3 + [h4] * n4 + [h5] * n5 + [h6] * n6 + [h7] * n7 + [h8] * n8 + [h9] * n9 + [h10] * n10,
    # # 15种箱子
    # 'p': [l1] * n1 + [l2] * n2 + [l3] * n3 + [l4] * n4 + [l5] * n5 + [l6] * n6 + [l7] * n7 + [l8] * n8 + [l9] * n9 + [l10] * n10 + [l11] * n11 + [l12] * n12 + [l13] * n13 + [l14] * n14 + [l15] * n15,
    # 'q': [w1] * n1 + [w2] * n2 + [w3] * n3 + [w4] * n4 + [w5] * n5 + [w6] * n6 + [w7] * n7 + [w8] * n8 + [w9] * n9 + [w10] * n10 + [w11] * n11 + [w12] * n12 + [w13] * n13 + [w14] * n14 + [w15] * n15,
    # 'r': [h1] * n1 + [h2] * n2 + [h3] * n3 + [h4] * n4 + [h5] * n5 + [h6] * n6 + [h7] * n7 + [h8] * n8 + [h9] * n9 + [h10] * n10 + [h11] * n11 + [h12] * n12 + [h13] * n13 + [h14] * n14 + [h15] * n15,
    'L': [L_box] * box_max,
    'W': [W_box] * box_max,
    'H': [H_box] * box_max
}
# # 3种箱子
volume_num = l1 * w1 * h1 * n1 + l2 * w2 * h2 * n2 + l3 * w3 * h3 * n3
# # 5种箱子
# volume_num = l1 * w1 * h1 * n1 + l2 * w2 * h2 * n2 + l3 * w3 * h3 * n3 + l4 * w4 * h4 * n4 + l5 * w5 * h5 * n5
# # 8种箱子
# volume_num = l1 * w1 * h1 * n1 + l2 * w2 * h2 * n2 + l3 * w3 * h3 * n3 + l4 * w4 * h4 * n4 + l5 * w5 * h5 * n5  + l6 * w6 * h6 * n6 + l7 * w7 * h7 * n7 + l8 * w8 * h8 * n8
# # 10种箱子
# volume_num = l1 * w1 * h1 * n1 + l2 * w2 * h2 * n2 + l3 * w3 * h3 * n3 + l4 * w4 * h4 * n4 + l5 * w5 * h5 * n5  + l6 * w6 * h6 * n6 + l7 * w7 * h7 * n7 + l8 * w8 * h8 * n8 + l9 * w9 * h9 * n9 + l10 * w10 * h10 * n10
# # 15种箱子
# volume_num = l1 * w1 * h1 * n1 + l2 * w2 * h2 * n2 + l3 * w3 * h3 * n3 + l4 * w4 * h4 * n4 + l5 * w5 * h5 * n5  + l6 * w6 * h6 * n6 + l7 * w7 * h7 * n7 + l8 * w8 * h8 * n8 + l9 * w9 * h9 * n9 + l10 * w10 * h10 * n10 + l11 * w11 * h11 * n11 + l12 * w12 * h12 * n12 + l13 * w13 * h13 * n13 + l14 * w14 * h14 * n14 + l15 * w15 * h15 * n15

"""
将上述货物和集装箱的尺寸，打包成两个三维列表矢量形式
"""
inputs = {'v':list(zip(inputs['p'], inputs['q'], inputs['r'])), 'V':list(zip(inputs['L'], inputs['W'], inputs['H']))}
print('货物的数量为:',len(inputs['v']))
print('集装箱（货车）的数量为:',len(inputs['V']))

# 记录下程序运行的开始时间
start_time = time.time()
# 可以使用上述自定义的inputs输入，也可以随机生成inputs输入数据
# inputs = generateInputs(80, 20, (600, 250, 250))
# 使用有偏随机密钥遗传算法和基于到货车车厢右上角最大距离的启发式规则解决三维装箱问题
model = BRKGA(inputs, num_generations=100, num_individuals=70, num_elites=10, num_mutants=7, eliteCProb=0.7)
model.fit(patient=15,verbose=True)
inputs['solution'] = model.solution
decoder = PlacementProcedure(inputs, model.solution, verbose=True)
# 输出使用集装箱（货车）的数量
print('使用的集装箱（货车）的数量为:',model.used_bins)
print('得到解程序所用时间为:',time.time() - start_time,'s')
# utilization_rate = (volume_num) / (int(model.used_bins) * L_box * W_box * H_box)
# print('三维装箱问题求解的利用率为：',utilization_rate)
print('每个货车中箱子总体积信息:', decoder.bin_used_volume)
for i in range(len(decoder.bin_used_volume)):
    utilization_rate_of_bin = decoder.bin_used_volume[i] / (L_box * W_box * H_box)
    print(f"第{i + 1}个货车空间利用率为：{utilization_rate_of_bin}")
print('适应度函数值:',decoder.evaluate())

def plot_history(history, tick=2):
    plt.figure(figsize=(10,4))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for target in ['mean', 'min']:
        plt.plot(history[target], label=target)
    plt.title('遗传迭代适应度变化曲线')
    plt.ylabel('适应度')
    plt.xlabel('遗传代数')
    plt.xticks(np.arange(0, len(history['min']), tick))
    plt.legend()
    for i in np.arange(math.ceil(min(history['min'])), int(max(history['mean'])) + 1):
        plt.axhline(y=i, color='g', linestyle='-')
    plt.show()
plot_history(model.history)

V = (587, 233, 220)
def draw(decoder):
    for i in range(decoder.num_opend_bins):
        container = plot_3D(V=V)
        for box in decoder.Bins[i].load_items:
            container.add_box(box[0], box[1], mode='EMS')
        print('集装箱（货车）', i + 1, ':')
        container.findOverlapping()
        container.show()
draw(decoder)
