import numpy as np
import torch
import matplotlib.pyplot as plt
from utility_functions import *
from pairOfClosestFactor import *
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
np.random.seed(2007)

### #### Multiple Plots for Random Shape and Pose Parameter ##########

### Randomly Generate Parameters #####

shape_coeffs = np.linspace(0.1,.9,1)
pose_coeffs = np.linspace(0.1,0.9,3)
total_plots = len(shape_coeffs)* len(pose_coeffs)
print("Total Plots: ", total_plots)
rows_plt,cols_plt = calc_closest_factors(total_plots)
fig = plt.figure()
plt_num = 1
for i_coeff in shape_coeffs:
    for j_coeff in pose_coeffs:
        pose_params = torch.rand(1, 63) * j_coeff
        dmpls_params = torch.rand(1, 10) * i_coeff
        beta = torch.rand(1,8)
        root_orient = torch.rand(1,3)
        body_mesh, joints = create_mesh(pose_params,beta,dmpls_params,root_orient)

        ax = fig.add_subplot(rows_plt,cols_plt,plt_num,projection="3d")
        createJoint(joints,ax,"CHeck")
        ####### Create poly3d #########
        ## Get the body_mesh which is a Trimesh object..
        mesh = Poly3DCollection(body_mesh.vertices[body_mesh.faces],alpha=0.5)
        ax.add_collection3d(mesh)
        ax.set_axis_off()
        # ax.view_init(azim= -49, elev=23)
        plt_num+=1
fig.suptitle("With Random Pose and Shape Parameters")
fig.savefig(f"Random_{total_plots}_plots.jpg")
# plt.show()


####### Multiple Plots for Random Shape and Pose Parameter ##########
pose_params = torch.rand(1, 63) * 0.52
dmpls_params = torch.rand(1, 10) * 0.03
beta = torch.rand(1,8)
root_orient = torch.rand(1,3)
body_mesh, joints = create_mesh(pose_params,beta,dmpls_params,root_orient)
fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")
#ax = Axes3D(fig)  ## used with poly3d
createJoint(joints,ax,"CHeck")
####### Create poly3d #########
## Get the body_mesh which is a Trimesh object..
mesh = Poly3DCollection(body_mesh.vertices[body_mesh.faces],alpha=0.5)
ax.add_collection3d(mesh)

limit_axis = 1.0
for axis in 'xyz':
    getattr(ax,'set_{}lim'.format(axis))(-limit_axis, limit_axis) ## Set limit of each axis
    getattr(ax,'set_{}label'.format(axis))(axis) ## Set label of each axis
ax.view_init(azim= 20, elev=-11)

plt.show()