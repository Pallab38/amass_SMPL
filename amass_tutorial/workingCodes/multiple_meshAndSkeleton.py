import matplotlib.pyplot as plt
import numpy as np
from utility_functions import *
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path  # to read the txt file containing poses.npz of all the datasets (HandBall, EyesJapan [for now])
import os


### Get the data ###
file_txt = Path("filePathToVisualize.txt").read_text()
## Convert the file into a list
file_txt = file_txt.splitlines()
### Plotting ###
total_plots = 6
rows = 2
cols = 3

#
# for i in range(0,len(file_txt)-total_plots,total_plots):
#     fig = plt.figure()
#     # axes = [fig.add_subplot(rows,cols, n+1,projection="3d") for n in range(total_plots)]
#     plt_num = 1
#     for j in range(i,i+total_plots):
#         if(plt_num>total_plots):
#             break
#         else:
#             ax1 = fig.add_subplot(rows,cols, plt_num, projection="3d")
#             plt_num +=1
#             ax2 = fig.add_subplot(rows,cols,plt_num)
#             plt_num +=1
#             single_file_path = file_txt[j]
#             print(single_file_path)
#             extract_path = os.path.split(single_file_path)[0]
#             dir_name = os.path.split(extract_path)[-1]
#             ## Load data
#             body_data = np.load(single_file_path)
#             ## Get body mesh and joint data
#             body_mesh,joints_data =extractData_createImg(body_data)
#             ####### Create poly3d #########
#             ## Get the body_mesh which is a Trimesh object..
#             mesh = Poly3DCollection(body_mesh.vertices[body_mesh.faces],alpha=0.5)
#
#             createJoint(joints_data,ax1,"Check")
#             ax1.add_collection3d(mesh)
#             ax1.set_axis_off()
#             dataset_name = extract_path.split("\\")[1]
#             print("dataset_name: ", dataset_name)
#
#             if(dataset_name =="Eyes_Japan_Dataset"):
#                 ax1.view_init(azim= 95, elev=4)
#                 # ax2.view_init(azim= 95, elev=4)
#             else:
#                 ax1.view_init(azim= -128, elev=4)
#                 # ax2.view_init(azim= -132, elev=4)
#             showBodyMeshOnly(body_mesh,ax2)
#             ax2.set_axis_off()
#
#
#     fig.suptitle(dir_name)
#     saving_path = Path("plots").joinpath(dataset_name)
#     print("saving_path: ",saving_path)
#     Path(saving_path).mkdir(parents=True, exist_ok=True)
#     plot_name = Path(saving_path).joinpath(dir_name+'.jpg')
#     print("plot_name",plot_name)
#
#     fig.savefig(plot_name)
#     # plt.show()
#     # plt.cla() ## clear the current axes
#     plt.close(fig)
#     # exit()
#



for i in range(0,len(file_txt)-total_plots,total_plots):
    fig = plt.figure()
    axes = [fig.add_subplot(rows,cols, n+1,projection="3d") for n in range(total_plots)]
    for j, ax in zip(range(i,i+total_plots),axes):
        single_file_path = file_txt[j]
        print(single_file_path)
        extract_path = os.path.split(single_file_path)[0]
        dir_name = os.path.split(extract_path)[-1]
        ## Load data
        body_data = np.load(single_file_path)
        ## Get body mesh and joint data
        body_mesh,joints_data =extractData_createImg(body_data)
        ####### Create poly3d #########
        ## Get the body_mesh which is a Trimesh object..
        mesh = Poly3DCollection(body_mesh.vertices[body_mesh.faces],alpha=0.5)
        createJoint(joints_data,ax,"Check")
        ax.add_collection3d(mesh)
        ax.set_axis_off()
        dataset_name = extract_path.split("\\")[1]
        print("dataset_name: ", dataset_name)
        if(dataset_name =="Eyes_Japan_Dataset"):
            ax.view_init(azim= 95, elev=4)
        else:
            ax.view_init(azim= -132, elev=4)
    fig.suptitle(dir_name)
    saving_path = Path("plots").joinpath(dataset_name+"01")
    print("saving_path: ",saving_path)
    Path(saving_path).mkdir(parents=True, exist_ok=True)
    plot_name = Path(saving_path).joinpath(dir_name+'.jpg')
    print("plot_name",plot_name)

    fig.savefig(plot_name)

    # plt.show()
    # plt.cla() ## clear the current axes
    plt.close(fig)
    # exit()


