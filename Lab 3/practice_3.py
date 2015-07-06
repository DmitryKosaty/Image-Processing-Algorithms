from numpy import *
import copy, cv2

IMAGE_SIZE = 256
FRAMES_COUNT = 10
ESC = 27

Palette = \
    [
        ('LIME',        [  0, 255,   0]), # 1
        ('YELLOW',      [  0, 255, 255]), # 2
        ('BLUE',        [255,   0,   0]), # 3
        ('MAGENTA',     [255,   0, 255]), # 4
        ('AQUA',        [255, 255,   0]), # 5
        ('CORN',        [93,  236, 251]), # 6
        ('GREEN',       [  0, 128,   0]), # 7
        ('OLIVE',       [  0, 128, 128]), # 8
        ('EMERALD',     [120, 200,  80]), # 9
        ('PURPLE',      [128,   0, 128]), # 10
        ('TEAL',        [128, 128,   0]), # 11
        ('GRAY',        [128, 128, 128]), # 12
        ('VIOLET',      [157,   0,  90]), # 13
        ('BROWN',       [ 42,  42, 165]), # 14
        ('CHOCOLATE',   [ 30, 105, 210]), # 15
        ('ORCHID',      [214, 112, 218]), # 16
        ('PINK',        [203, 192, 255]), # 17
        ('CHARTREUSE',  [153, 255, 153]), # 18
        ('CERULEAN',    [167, 123,   0]), # 19
        ('ORANGE',      [  0, 153, 255])  # 20
    ]
 
DictColors = dict([[Palette.index(color), color] for color in Palette])
 
Image = zeros((IMAGE_SIZE, IMAGE_SIZE, 3), uint8)
 
def X(t):
    return IMAGE_SIZE * t / float(FRAMES_COUNT)
 
def Y(x):
    return x, 0.5 * x
 
def ChangeCoord(node):
    for ind1 in range(-1, 1):
        for ind2 in range(-1, 1):
            Image[node[0] + ind1][node[1] + ind2] = [255, 255, 255]
 
class Trajectory:
    def __init__(self, path):
        self.path = path
    def __repr__(self):
        return '%s' % self.path
    def AppendNode(self, node):
        self.path.append(node)
    def GetNodes(self):
        result =[]
        for node in self.path:
            result.append(node)
        return result
    def Draw(self, color):
        node_temp = self.path[0]
        for node in self.path[1:]:
            cv2.line(Image, (int(node_temp[1]), int(node_temp[0])), (int(node[1]), int(node[0])), color)
            node_temp = node
 
class Hypothesis:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def __repr__(self):
        return 'Hypothesis: (%s, %s)' % (self.first, self.second)
    def AppendNodes(self, node_1, node_2):
        self.first.AppendNode(node_1)
        self.second.AppendNode(node_2)
    def GetNodes(self):
        return self.first.GetNodes()
    def Draw(self, color):
        self.first.Draw(color)
        self.second.Draw(color)
 
def GenerationHypotheses(node_1, node_2):
    result = []
    for hypothesis in hypotheses:
        hypothesis_1 = copy.deepcopy(hypothesis)
        hypothesis_1.AppendNodes(node_1, node_2)
        result.append(hypothesis_1)
        hypothesis_2 = hypothesis
        hypothesis_2.AppendNodes(node_2, node_1)
        result.append(hypothesis_2)
    return result
 
def OrdinaryLeastSquares(A, y):
    A_tr = A.transpose()
    M_1 = A_tr.dot(A)
    M_inv = linalg.inv(M_1)
    M_2 = M_inv.dot(A_tr)
    x = M_2.dot(y)
    return x
 
def CalcRating(nodes):
    x = zeros(5)
    A = ones((5,2))
    y = zeros(5)
    for cnt in xrange(5):
        index = (len(nodes) - 1) + cnt - 4
        x[cnt] = nodes[index][0]
        A[cnt, 0] = x[cnt]
        y[cnt] = nodes[index][1]
    k, b = OrdinaryLeastSquares(A, y)
    rating = 0.
    for i in xrange(5):
        rating += ((k * x[i] + b) - y[i]) ** 2
    if rating < 0.1:
        rating = 0.
    return rating
 
def Top20Hypotheses(hypotheses):
    list = []
    for hypothesis in hypotheses:
        last_five_nodes = hypothesis.GetNodes()
        rating = CalcRating(last_five_nodes)
        list.append((rating, hypothesis))
    sorted_list = sorted(list, key = lambda x: x[0])
    best_hypotheses = []
    for item in sorted_list[:20]:
        best_hypotheses.append(item[1])
    return best_hypotheses
 
hypotheses = []
 
for t in range(FRAMES_COUNT):
    x = X(t)
    y = Y(x)
    node_1, node_2 = (x, y[0]), (x, y[1])
    ChangeCoord(node_1)
    ChangeCoord(node_2)
    if t == 0:
        track_1 = Trajectory([node_1])
        track_2 = Trajectory([node_2])
        hypothesis = Hypothesis(track_1, track_2)
        hypotheses.append(hypothesis)
        continue
    if t == 1:
        hypotheses[0].AppendNodes(node_1, node_2)
        continue
    hypotheses = GenerationHypotheses(node_1, node_2)
    if len(hypotheses) >= 20:
        hypotheses = Top20Hypotheses(hypotheses)
        for hypothesis in hypotheses[1:]:
            color = DictColors.values()[hypotheses.index(hypothesis)][1]
            hypothesis.Draw(color)
        hypotheses[0].Draw([0, 0, 255])
 
cv2.imshow("", Image)
key = cv2.waitKey()
if key == ESC:
    cv2.destroyAllWindows()
elif key == ord('s'):
    cv2.imwrite('Image.png', Image)
    cv2.destroyAllWindows()
