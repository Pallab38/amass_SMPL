import numpy as np
import matplotlib.pyplot as plt

from funcForSkeleton import *

bodyData_path = r"Data/bodyData/BMLhandball/S01_Expert/Trial_upper_left_005_poses.npz"
body_data = np.load(bodyData_path)
body_mesh,joints_data =extractData_createImg(body_data)
#thetas = [np.radians(90),np.radians(120), np.radians(45),np.radians(180)]  # np.pi/2 #
fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")
#ax.add_collection3d(body_mesh)
theta = -np.radians(45)
rot_mat =createRotationMatrix(theta)
new_joints_data = joints_data @ rot_mat
createJoint(joints_data,ax,"CHeck")
plt.show()