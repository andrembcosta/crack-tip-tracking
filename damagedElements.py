import pyvista as pv

def getDamagedElements(vtkFile, threshold):
    data = pv.read(vtkFile)
    data = data[0][0]
    data.set_active_scalars('d')
    data = data.point_data_to_cell_data()
    elementalDamageList = data.cell_data['d']
    damagedElements = []
    for i in range(len(elementalDamageList)):
        if elementalDamageList[i] > threshold:
            damagedElements.append(i)
    return damagedElements

