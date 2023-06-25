import os
from time import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyevtk.hl import pointsToVTK, gridToVTK
from scipy.interpolate import griddata, Rbf

def grid_vel(data, deltax=20, deltay=20, deltaz=20, interp_method="rbf"):
    data = pd.read_csv(data)
    # Reformat data to numpy array
    x = data['X'].values
    y = data['Y'].values
    z = data['Z'].values
    vp = data['Vp'].values
    vs = data['Vs'].values
    vp_vs = data['Vp/Vs'].values

    # Create spatial grid
    grid_x, grid_y, grid_z = np.meshgrid(np.arange(min(x), max(x)+1, deltax),
                                         np.arange(min(y), max(y)+1, deltay),
                                         np.arange(min(z), max(z)+1, deltaz))

    # Interpolate Vp, Vs, Vp/Vs
    if interp_method == "linear":
        grid_vp = griddata((x, y, z), vp, (grid_x, grid_y, grid_z), method='linear')
        grid_vs = griddata((x, y, z), vs, (grid_x, grid_y, grid_z), method='linear')
        grid_ps = griddata((x, y, z), vp_vs, (grid_x, grid_y, grid_z), method='linear')

    if interp_method == "rbf":
        grid_vp = Rbf(x, y, z, vp, function="thin_plate")(grid_x, grid_y, grid_z)
        grid_vs = Rbf(x, y, z, vs, function="thin_plate")(grid_x, grid_y, grid_z)
        grid_ps = Rbf(x, y, z, vp_vs, function="thin_plate")(grid_x, grid_y, grid_z)
    return grid_x, grid_y, grid_z, grid_vp, grid_vs, grid_ps

def create_vts(x, y, z, vp, vs, ps, nama_file="tomogram"):
    gridToVTK(nama_file, x, y, z, pointData={"Vp": vp, "Vs": vs, "Vp/Vs": ps})