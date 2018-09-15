from src import FEMTruss as t
import math as m
import numpy as np

# Assign value to the local matrix
# Local configuration as the base of all elements
mat = t.LocalMatrix(1, 1, 1)
# Construct the local matrix
mat.matrixConstructor()
# Return the result of the constructed local matrix
localMat = mat.getMatrix()
# Print the results
#print(localMat)
# For element 3
mat3 = t.LocalMatrix(1, 1, m.sqrt(2))
mat3.matrixConstructor()
localMat3 = mat3.getMatrix()

# Return transformation matrix of each element as an array
def transformationMatrixController(angle1, angle2, angle3, numOfEl):
    tMatrices = []
    d = {'angle1': angle1,
         'angle2': angle2,
         'angle3': angle3}
    for i in range(0, numOfEl):
        m = t.TransformationMatrix(d.get('angle' + str(i + 1)))
        m.matrixConstructor()
        tMatrices.append(m.getMatrix())
    return tMatrices

# Return global matrix of each element as an array
def elementGlobalMatrixController(localMatrix, transMatrices):
    globalMatrices = []
    for tmatrix in transMatrices:
        mat = t.GlobalMatrix(localMatrix, tmatrix)
        mat.matrixConstructor()
        globalMatrices.append(mat.getMatrix())
    return globalMatrices


# Assemble the global force vector
forceVector = np.array([[0, 1, 0, 0, 0, 0]]).T

transMatrices = transformationMatrixController(0, m.pi * 3 / 2, m.radians(315), 3)

elementGlobalMatrices = elementGlobalMatrixController(localMat, transMatrices)
# Amend element 3
mat = t.GlobalMatrix(localMat3, transMatrices[2])
mat.matrixConstructor()
elementGlobalMatrices[2] = mat.getMatrix()
# Assign value to each element to its global configuration
element1GL = elementGlobalMatrices[0]
element2GL = elementGlobalMatrices[1]
element3GL = elementGlobalMatrices[2]

# Assemble the elements and return the global stiffness matrix of the system
globalMat = np.empty([6, 6])
globalMat[0:2, 0:2] = element1GL[0:2, 0:2] + element3GL[0:2, 0:2]
globalMat[0:2, 2:4] = element1GL[0:2, 2:4]
globalMat[2:4, 0:2] = element1GL[2:4, 0:2]
globalMat[2:4, 2:4] = element1GL[2:4, 2:4] + element2GL[0:2, 0:2]
globalMat[2:4, 4:6] = element2GL[0:2, 2:4]
globalMat[4:6, 2:4] = element2GL[2:4, 0:2]
globalMat[4:6, 4:6] = element2GL[2:4, 2:4] + element3GL[2:4, 2:4]
globalMat[0:2, 4:6] = element3GL[0:2, 2:4]
globalMat[4:6, 0:2] = element3GL[2:4, 0:2]
#t.matprint(globalMat)
#print(t.isSymmetrical(globalMat))
# Since DOF 4, 5, 6 has a known displacement of 0, the system can be reduced to  a 3x3 matrix
reducedMatFinal = globalMat[0:3, 0:3]
reducedForceVector = forceVector[0:3]
t.matprint(reducedMatFinal)
#print(np.linalg.det(reducedMatFinal))
# Calculate the displacements at each free node
displacements = np.matmul(np.linalg.inv(reducedMatFinal), reducedForceVector)
#t.matprint(displacements)
