from numpy import *
import cv2

IMAGE_SIZE = 256
g = 9.8
FRAMES_COUNT = int(sqrt(2. * IMAGE_SIZE / float(g)))
X0, Y0 = 1., 1.
Vx = (IMAGE_SIZE - X0) / float(FRAMES_COUNT)
WHITE = [255, 255, 255]
RED = [0, 0, 255]

def X(t):
    return Y0 + 0.5 * (g * t * t)

def Y(t):
    return X0 + Vx * t

def ChangeCoord(obj_center, color):
    for shift_x in range(-1, 1):
        for shift_y in range(-1, 1):
            Image[int(obj_center[0]) + shift_x][int(obj_center[1]) + shift_y] = color

class KalmanFilter:
    def __init__(self, A, H, Sigma_w, Sigma_v):
        self.A = A
        self.H = H
        self.Sigma_w = Sigma_w
        self.Sigma_v = Sigma_v
    def Predict(self, x_previous, P_previous):
        x_predict = self.A * x_previous
        P_predict = self.A * P_previous * self.A.T + self.Sigma_w
        return x_predict, P_predict
    def Correct(self, x_predict, P_predict, z):
        S = self.H * P_predict * self.H.T + self.Sigma_v
        y = z - self.H * x_predict
        K = P_predict * self.H.T * S.I
        x_correct = x_predict + K * y
        P_correct = (eye(4) - K * self.H) * P_predict
        return x_correct, P_correct

Image = zeros((IMAGE_SIZE, IMAGE_SIZE, 3))

A = matrix([[1., 0., 1., 0.],
            [0., 1., 0., 1.],
            [0., 0., 1., 0.],
            [0., 0., 0., 1.]])

H = matrix([[1., 0., 0., 0.],
            [0., 1., 0., 0.]])

Sigma_w = eye(4) * 10

Sigma_v = eye(2) * 0.1

filter = KalmanFilter(A, H, Sigma_w, Sigma_v)

x_iters = matrix(zeros(4)).T
x_iters[0], x_iters[1] = X(0), Y(0)

P = eye(4)

x = matrix(zeros(4)).T

for t in range(FRAMES_COUNT):
    print 't =', t
    x[0], x[1] = X(t), Y(t)
    print 'real coords = %f, %f' % (x[0, 0], x[1, 0])
    x_predict, P_predict = filter.Predict(x_iters, P)
    w = matrix(random.multivariate_normal([0., 0., 0., 0.], Sigma_w)).T
    v = matrix(random.multivariate_normal([0., 0.], Sigma_v)).T
    z = H * (A * x + w) + v
    x_correct, P_correct = filter.Correct(x_predict, P_predict, z)
    print 'filtered coords = %f, %f' % (x_correct[0, 0], x_correct[1, 0])
    x_iters[:2, 0] = x_correct[:2, 0]
    P = P_correct
    ChangeCoord(x[:2], WHITE)
    ChangeCoord(x_iters[:2], RED)
cv2.imshow("", Image), cv2.waitKey()