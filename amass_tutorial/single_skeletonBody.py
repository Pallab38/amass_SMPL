import numpy as np
import matplotlib.pyplot as plt
from myFunctions import *
import open3d as o3
#### Show Image  ###
#from tools import show_image

bodyData_path = r"Data/bodyData/BMLhandball/S01_Expert/Trial_upper_left_005_poses.npz"
body_data = np.load(bodyData_path)
body_mesh,joints_data,joints_mesh =extractData_createImg(body_data,True)
#
#o3.visualization.draw_geometries([body_mesh])
jointData_fromMesh = []
for i in range(len(joints_mesh)):
    print(joints_mesh[i].vertices.shape)
    jointData_fromMesh.append(joints_mesh[i].vertices[1])
print(joints_data.shape)
jointData_fromMesh = np.array(jointData_fromMesh)
print(jointData_fromMesh.shape)

plotting_cv2(body_mesh,joints_data)