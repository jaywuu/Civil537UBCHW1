from src import FEMBeam as b
import numpy as np
import math as m

E = 60 * 10 ** 6 # 60 GPa
I = 2 * 10 ** (-4) # 2*10^(-4) m^4
L = 5 # 5 m
kSpring = 100 # 100 kN/m
forceVector = np.array([[-15, 0, 0, 0]]).T
#b.matprint((forceVector))
# Upward and ccw positive
def localMatrixController():
    localMatrix = b.LocalMatrix(E, I, L)
    localMatrix.matrixConstructor()
    return localMatrix.getMatrix()


def systemMatrixController(mat):
    systemMatrix = np.empty([4, 4])
    systemMatrix[0, 0] = mat[0, 0] * 2
    systemMatrix[0, 1] = mat[0, 1] + mat[2, 3]
    systemMatrix[1, 0] = mat[1, 0] + mat[3, 2]
    systemMatrix[1, 1] = mat[1, 1] * 2

    systemMatrix[0, 2] = mat[2, 1]
    systemMatrix[0, 3] = mat[0, 3]
    systemMatrix[1, 2] = mat[3, 1]
    systemMatrix[1, 3] = mat[1, 3]
    systemMatrix[2, 0] = mat[1, 2]
    systemMatrix[2, 1] = mat[1, 3]
    systemMatrix[3, 0] = mat[3, 0]
    systemMatrix[3, 1] = mat[3, 1]
    systemMatrix[2, 2] = mat[1, 1]
    systemMatrix[3, 3] = mat[3, 3]
    systemMatrix[2, 3] = 0
    systemMatrix[3, 2] = 0
    return systemMatrix


def calcDispl(matK, matF):
    return np.matmul(np.linalg.inv(matK), matF)


def localDispl(displ, element):
    newDipsl = np.empty([4, 1])
    if element == 1:
        newDipsl[0] = 0
        newDipsl[1] = displ[2]
        newDipsl[2] = displ[0]
        newDipsl[3] = displ[1]
    elif element == 2:
        newDipsl[0] = displ[0]
        newDipsl[1] = displ[1]
        newDipsl[2] = 0
        newDipsl[3] = displ[3]
    return newDipsl


def calcElementForce(kMat, displ):
    return np.matmul(kMat, displ)

localMatrix = localMatrixController()
systemMatrix = systemMatrixController(localMatrix)
# After adding stiffness from the spring
systemMatrix[0, 0] = systemMatrix[0, 0] + 100
# Calculate displacement and slope
displacement = calcDispl(systemMatrix, forceVector)
displ1 = localDispl(displacement, 1)
displ2 = localDispl(displacement, 2)

elementForce1 = calcElementForce(localMatrix, displ1)
elementForce2 = calcElementForce(localMatrix, displ2)

# Print results
b.matprint(systemMatrix)
b.matprint(localMatrix)
b.matprint(displacement)
print(b.isSymmetrical(systemMatrix))
b.matprint(displ1)
b.matprint(displ2)
b.matprint(elementForce1)
b.matprint(elementForce2)
print(elementForce2[0] * 2 + 100 * displacement[0])