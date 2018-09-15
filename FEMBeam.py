import numpy as np
import math as m

class Matrix:
    # Global method for returning the matrix
    def getMatrix(self):
        return self.matrix

class LocalMatrix(Matrix):
    # Initialization
    def __init__(self, E, I, L):
        self.E = E
        self.I = I
        self.L = L

    # Construct local matrix
    # This constructor contains the local matrix
    def matrixConstructor(self):
        localMatrix = np.array([[12, 6*self.L, -12, 6*self.L],
                                [6*self.L, 4*self.L**2, -6*self.L, 2*self.L**2],
                               [-12, -6*self.L, 12, -6*self.L],
                               [6*self.L, 2*self.L**2, -6*self.L, 4*self.L**2]])
        # print(localMatrix)
        self.matrix = self.E * self.I / self.L ** 3 * localMatrix


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