import numpy as np
from shaders import SN_POSITION_NAME
def create_vertice_array(n_points,dim=2):
    return np.zeros(n_points, [(SN_POSITION_NAME, np.float32, dim)])
