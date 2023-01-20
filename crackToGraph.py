import pyvista as pv
import networkx as ntx
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix
from damagedElements import *

def testNeighbors(mesh, elemIndexA, elemIndexB):
    setA = set(mesh.cell_point_ids(elemIndexA))
    setB = set(mesh.cell_point_ids(elemIndexB))
    commonPoints = set.intersection(setA,setB)
    if len(commonPoints) == 2:
        return 1
    else:
        return 0

filename = 'cracks_and_graphs/vtk_data/branch_vtk_data_5.vtm'
#only needed in first time step
data = pv.read(filename)
data = data[0][0]
posList = data.cell_centers().points
pos = dict(zip(range(data.n_cells),posList[:,:2]))
numCells = data.n_cells
print(numCells)
#meshConnections = meshAdjacency(filename)
##
#repeat every time step
damagedCells = getDamagedElements(filename, 0.9)
print(len(damagedCells))
graphAdjacency = lil_matrix((numCells,numCells)) #build sparse matrix
for i in damagedCells:
    for j in damagedCells:
        graphAdjacency[i,j] = testNeighbors(data, i, j)
G = ntx.Graph(graphAdjacency)

ntx.draw(G, with_labels = False, pos=pos)
plt.show()      



