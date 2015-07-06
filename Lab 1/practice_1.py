from numpy import *
import cv2

IMAGE_SIZE = 256

def SumByModuloTwo(a, b):
    if a + b == 1:
        return 1
    else:
        return 0

def NoiseCreation(p):
    V = zeros((IMAGE_SIZE, IMAGE_SIZE))
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            if random.random() < p:
                V[i, j] = 1
    return V

def NoiseImprose(I, V):
    J = zeros((IMAGE_SIZE, IMAGE_SIZE))
    for i in range(1, IMAGE_SIZE - 1):
        for j in range(1, IMAGE_SIZE - 1):
            J[i, j] = SumByModuloTwo(I[i, j], V[i, j])
    return J

def Filter(J):
    for i in range(1, IMAGE_SIZE - 1):
        for j in range(1, IMAGE_SIZE - 1):
            if J[i, j] == 1 and J[i + 1, j] == 0 and J[i, j + 1] == 0 and J[i - 1, j] == 0 and J[i, j - 1] == 0:
                J[i, j] = 0
    return J

def Rates(W, I, (i, j), p):
    global TP, TN, FN, FP
    global P_TP, P_TN, P_FN, P_FP
    if W[i][j] == I[i][j]:
        if I[i][j] == 1:
            TP += 1
            P_TP = (1 - p) * (1 - p * power(1 - p, 3))
        else:
            TN += 1
            P_TN = (1 - p) * (1 + p * power(1 - p, 3))
    else:
        if I[i][j] == 1:
            FN += 1
            P_FN = p * (1 + power(1 - p, 4))
        else:
            FP += 1
            P_FP = p * (1 - power(1 - p, 4))

def Experiment(W, I, p):
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            Rates(W, I, (i, j), p)

I = zeros((IMAGE_SIZE, IMAGE_SIZE))

ships_count = 10
print 'ships count =', ships_count

for cnt in range(ships_count):
    point_1 = (random.randint(2, IMAGE_SIZE - 2), random.randint(2, IMAGE_SIZE - 2))
    if random.random() < 0.5:
        dx = 0
        if random.random() < 0.5:
            dy = -1
        else:
            dy = 1
    else:
        dy = 0
        if random.random() < 0.5:
            dx = -1
        else:
            dx = 1
    point_2 = (point_1[0] + dx, point_1[1] + dy)
    I[point_1] = 1
    I[point_2] = 1

cv2.imshow("", I), cv2.waitKey(), cv2.destroyAllWindows()

print 'p =',
p = float(input())

print 'experiments_count =',
experiments_count = int(input())

TP, TN, FN, FP = 0, 0, 0, 0
P_TP, P_TN, P_FN, P_FP = 0, 0, 0, 0

for experiment_number in range(experiments_count):
    V = NoiseCreation(p)
    J = NoiseImprose(I, V)
    W = Filter(J)
    Experiment(W, I, p)

R_TP = TP / float (2 * ships_count * experiments_count)
R_TN = TN / float ((IMAGE_SIZE * IMAGE_SIZE - 2 * ships_count) * experiments_count)
R_FN = FN / float (2 * ships_count * experiments_count)
R_FP = FP / float ((IMAGE_SIZE * IMAGE_SIZE - 2 * ships_count) * experiments_count)
print 'True Positive =', TP
print 'P(TP) = %8.8f' % R_TP, 'P`(TP) = %8.8f' % P_TP
print 'True Negative =', TN
print 'P(TN) = %8.8f' % R_TN, 'P`(TN) = %8.8f' % P_TN
print 'False Negative =', FN
print 'P(FN) = %8.8f' % R_FN, 'P`(FN) = %8.8f' % P_FN
print 'False Positive = ', FP
print 'P(FP) = %8.8f' % R_FP, 'P`(FP) = %8.8f' % P_FP
print 'Foreground : P(TP) + P(FN) = %8.8f'%(R_TP + R_FN), 'P`(TP) + P`(FN) = %8.8f'%(P_TP + P_FN)
print 'Background : P(TN) + P(FP) = %8.8f'%(R_TN + R_FP), 'P`(TN) + P`(FP) = %8.8f'%(P_TN + P_FP)