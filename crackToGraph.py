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

tips=set()
filename = 'vtk_data/branch_vtk_data_13.vtm'
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
damagedCells = getDamagedElements(filename, 0.98)
numDamagedCells = len(damagedCells)
print(len(damagedCells))
graphAdjacency = lil_matrix((numDamagedCells,numDamagedCells)) #build sparse matrix
npos = {}
for i in range(len(damagedCells)):
    npos[i]=pos[damagedCells[i]]
    for j in range(len(damagedCells)):
        graphAdjacency[i,j] = testNeighbors(data, damagedCells[i], damagedCells[j])
G = ntx.Graph(graphAdjacency)
#loop over G, if node has degree 1, store its position
degrees = [val for (node, val) in G.degree()]

for i in range(degrees):
    if degrees[i]==1:
        tips.add(npos[i])

ntx.draw(G, with_labels = False, pos=npos, node_size=30)
plt.show()      
