import numpy as np
import pylab
import cv2

def OrdinaryLeastSquares(A, y):
    return (np.linalg.inv(A.transpose().dot(A)).dot(A.transpose())).dot(y)

try:
    img_1 = cv2.imread("cones/disp2.png", 0)
    # cv2.imshow("disp2.png", img_1); cv2.waitKey(); cv2.destroyWindow("disp2.png")

    img_2 = cv2.imread("cones/disp6.png", 0)
    # cv2.imshow("disp6.png", img_2); cv2.waitKey(); cv2.destroyWindow("disp6.png")
except cv2.error as error:
    print error.message

disparities_set = np.ndarray(shape=(img_1.shape[0],), dtype=float)

for i in range(img_1.shape[0]):

    print "i =",i+1

    A = np.ones(shape=(img_1.shape[1],2))
    y = np.ndarray(shape=(img_1.shape[1],), dtype=float)

    response_func = {}

    for d in range(img_1.shape[1]):

        response_func[d] = 0

        for j in range(img_1.shape[1]):
            response_func[d] += np.power((img_1[i,j] - img_2[i,j-d]), 2)

        A[d,0] = d
        y[d] = response_func[d]

    disparities_set[i] = OrdinaryLeastSquares(A, y)[1]

    # pylab.plot(response_func.keys(), response_func.values(), 'ro-')
    # pylab.show()

file = open('results.txt', 'w')

for u in range(img_1.shape[0]):
    for v in range(img_1.shape[1]):
        X = np.ndarray(shape=(img_1.shape[0],), dtype=float)
        Y = np.ndarray(shape=(img_1.shape[0],), dtype=float)
        Z = np.ndarray(shape=(img_1.shape[0],), dtype=float)
        for k in range(img_1.shape[0]):
            X[k] = u - 0.5*img_1.shape[0]
            Y[k] = v - 0.5*img_1.shape[1]
            Z[k] = 1000/float(disparities_set[k])
            file.write("%f %f %f\n" % (X[k], Y[k], Z[k]))