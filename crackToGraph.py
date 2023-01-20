import pyvista as pv
import networkx as ntx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

graphs = [] # some array of graphs
NPOS = []
COLORS =[]
NSIZEMAP=[]
fig = plt.figure()
for i in range(4,20):
    tips=[]
    #filename = 'vtk_data/branch_vtk_data_15.vtm'
    filename = 'vtk_data/branch_vtk_data_'+str(i)+'.vtm'
    print(filename)
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
    #ensure connectivity

    thresholdList = [0.99, 0.98, 0.97, 0.96, 0.95]
    for threshold in thresholdList:

        damagedCells = getDamagedElements(filename, threshold)
        numDamagedCells = len(damagedCells)
        print(len(damagedCells))
        graphAdjacency = lil_matrix((numDamagedCells,numDamagedCells)) #build sparse matrix
        npos = {}
        for i in range(len(damagedCells)):
            npos[i]=pos[damagedCells[i]]
            for j in range(len(damagedCells)):
                graphAdjacency[i,j] = testNeighbors(data, damagedCells[i], damagedCells[j])
        G = ntx.Graph(graphAdjacency)
        if ntx.is_connected(G):
            break    

    print(threshold)
    #loop over G, if node has degree 1, store its position
    degrees = [val for (node, val) in G.degree()]
    psieList = data.cell_data['psie_active']
    psic = 190
    tips_index = []
    tips_psie = []
    for i in range(len(degrees)):
        if degrees[i]==1:
            if psieList[damagedCells[i]] > psic:
                tips.append(npos[i])
                tips_index.append(i)
                tips_psie.append(psieList[damagedCells[i]])

    #color tips
    color_map = ['red' if node in tips_index else 'blue' for node in G]  
    node_size_map =  [40 if node in tips_index else 1 for node in G]       

    #ntx.draw(G, with_labels = False, pos=npos, node_size=node_size_map, node_color=color_map)
    print(tips_psie)
    print(len(tips))
    #fig = plt.figure()
    #ntx.draw(G, with_labels = False, pos=npos, node_size=node_size_map, node_color=color_map)
    graphs.append(G)
    NPOS.append(npos)
    COLORS.append(color_map)
    NSIZEMAP.append(node_size_map)
    #nodes = ntx.draw_networkx_nodes(G,npos, node_size=node_size_map, node_color=color_map)
    #nodeFrames.append(nodes)
    #edges = ntx.draw_networkx_edges(G,npos)

#ntx.draw(graphs[5], with_labels = False, pos=npos, node_size=node_size_map, node_color=color_map)
def update(i):
    fig.clear()
    plt.xlim(-1,1)
    plt.ylim(-0.7,0.7)
    ntx.draw(graphs[i], with_labels = False, pos=NPOS[i], node_size=NSIZEMAP[i], node_color=COLORS[i])

fig = plt.gcf()
ani = animation.FuncAnimation(fig, update, frames=len(graphs), interval=300, repeat_delay=300, repeat=True)
ani.save('movie.gif')
plt.show()    
