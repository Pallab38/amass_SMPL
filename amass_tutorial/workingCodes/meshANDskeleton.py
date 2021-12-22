import matplotlib.pyplot as plt
import numpy as np
# from utility_functions import *
import utility_functions
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# bodyData_path = r"../Data/bodyData\Eyes_Japan_Dataset\takiguchi\turn-01-call-takiguchi_poses.npz"
bodyData_path=r"../Data/bodyData\BMLhandball\S01_Expert\Trial_upper_left_012_poses.npz"
body_data = np.load(bodyData_path)




body_mesh,joints_data = utility_functions.extractData_createImg(body_data)

fig = plt.figure()
ax = fig.add_subplot(121,projection="3d")
#ax = Axes3D(fig)  ## used with poly3d
# utility_functions.createJoint(joints_data,ax,"CHeck")
####### Create poly3d #########
## Get the body_mesh which is a Trimesh object..
vertices = body_mesh.vertices
faces = body_mesh.faces

mesh = Poly3DCollection(body_mesh.vertices[body_mesh.faces],alpha=0.5)
# face_color = (141 / 255, 184 / 255, 226 / 255)
# edge_color = (50 / 255, 50 / 255, 50 / 255)
# mesh.set_edgecolor(edge_color)
# mesh.set_facecolor(face_color)
ax.add_collection3d(mesh)

# limit_axis = 1.0
# for axis in 'xyz':
#     getattr(ax,'set_{}lim'.format(axis))(-limit_axis, limit_axis) ## Set limit of each axis
#     getattr(ax,'set_{}label'.format(axis))(axis) ## Set label of each axis

# ax.view_init(azim= 95, elev=4)
ax.view_init(azim= -132, elev=4)
# ax.set_axis_off()
ax2 = fig.add_subplot(122)
utility_functions.showBodyMeshOnly(body_mesh,ax2)
ax2.set_axis_off()
fig.suptitle("HandBall_S01_Expert_upperleft")
# fig.savefig("HandBall_S01_Expert_upperleft.jpg")
plt.show()