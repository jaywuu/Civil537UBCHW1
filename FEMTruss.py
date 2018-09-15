import numpy as np
import math as m

class Matrix:
    # Global method for returning the matrix
    def getMatrix(self):
        return self.matrix

class LocalMatrix(Matrix):
    # Initialization
    def __init__(self, E, A, L):
        self.E = E
        self.A = A
        self.L = L

    # Construct local matrix
    # This constructor contains the local matrix
    def matrixConstructor(self):
        localMatrix = np.array([[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]])
        # print(localMatrix)
        self.matrix = self.A * self.E / self.L * localMatrix


class TransformationMatrix(Matrix):

    # Initialization
    def __init__(self, angle):
        self.angle = angle

    # Construct transformation matrix
    # This constructor contains the transformation matrix
    def matrixConstructor(self):
        self.matrix = np.array([[m.cos(self.angle), m.sin(self.angle), 0, 0],
                                [-m.sin(self.angle), m.cos(self.angle), 0, 0],
                                [0, 0, m.cos(self.angle), m.sin(self.angle)],
                                [0, 0, -m.sin(self.angle), m.cos(self.angle)]])


class GlobalMatrix(Matrix):
    # Initialization
    def __init__(self, lclMat, transMat):
        self. lclMat = lclMat
        self.transMat = transMat

    # Construct transformation matrix using local matrix and transformation matrix
    def matrixConstructor(self):
        #print(transpose(self.transMat, 4))
        self.matrix = np.matmul(transpose(self.transMat, 4), self.lclMat)
        self.matrix = np.matmul(self.matrix, self.transMat)

# Effects: returns a transposed square matrix with given sizes
def transpose(matrix, size):
    newMat = np.empty([size, size])
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            newMat[i, j] = matrix[j, i]
    return newMat

# Effects: returns true if the matrix is symmetrical, else returns false
def isSymmetrical(mat):
    key = False
    for i in range(0, mat.shape[0]):
        for j in range(0, mat.shape[1]):
            if mat[i, j] != mat[j, i]:
                key = False
                break
            elif mat[i, j] == mat[j, i]:
                key = True
    return key

# Printer
def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="  ")
        print("")
    print('-----------------------')