import torch
import numpy as np
import matplotlib.pyplot as plt
import cv2
from human_body_prior.tools.omni_tools import copy2cpu as c2c
#### Body Model ## ### https://github.com/nghorbani/human_body_prior
from human_body_prior.body_model.body_model import BodyModel

#### For MESH   ##
import trimesh
from human_body_prior.mesh import MeshViewer
from human_body_prior.tools.omni_tools import  colors
from human_body_prior.mesh.sphere import points_to_spheres

### To Rotate Global Orientation
from human_body_prior.tools.omni_tools import apply_mesh_tranfsormations_


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def body_model():
    body_model_path = r"C:\Users\shunn0\Desktop\THESIS\TASK01\code\amass_tutorial\Data\bodyModels\smplh\male\model.npz"
    dmpl_path = r"C:\Users\shunn0\Desktop\THESIS\TASK01\code\amass_tutorial\Data\bodyModels\dmpl\male\model.npz"
    num_betas = 10
    num_dmpls = 8
    bm = BodyModel(bm_path=body_model_path, num_betas=num_betas, num_dmpls=num_dmpls, path_dmpl=dmpl_path)

    return bm

def create_mesh(body,  beta=torch.zeros((1,8)).to(device), dmpls=torch.zeros((1,3)).to(device),
                root_orient=torch.zeros((1,3)).to(device), hand=torch.zeros((1,90)).to(device)):
    ## Mesh Viewer Set up
    # imw, imh = 1600, 1600
    # mv = MeshViewer(width=imw, height=imh)
    bm = body_model()
    face = c2c(bm.f)  ## np.array(13776,3) from torch.Tensor([13776, 3]# )
    body = bm(pose_body=body, pose_hand=hand, betas=beta, dmpls=dmpls, root_orient=root_orient)
    num_vertices = body.v[0].shape[0]

    body_mesh = trimesh.Trimesh(vertices=c2c(body.v[0]), faces=face,
                                vertex_colors=np.tile(colors['grey'], (num_vertices, 1)),
                                process=False)

    joint_data = c2c(body.Jtr[0])  # (52, 3)
    # joint_mesh = points_to_spheres(joint_data, vc=colors['red'], radius=0.005)
    # apply_mesh_tranfsormations_(([body_mesh] + joint_mesh), trimesh.transformations.rotation_matrix(120, (0, 0, 1)))
    # apply_mesh_tranfsormations_(([body_mesh] + joint_mesh), trimesh.transformations.rotation_matrix(30, (1, 0, 0)))
    # mv.set_static_meshes(([body_mesh] + joint_mesh))
    # body_img = mv.render(render_wireframe=True)

    return body_mesh,joint_data


def extractData_createImg(body_data):
    frame_num =1
    root_orient = torch.Tensor(body_data['poses'][frame_num:frame_num + 1, :3]).float().to(device)
    pose_body = torch.tensor(body_data['poses'][frame_num:frame_num + 1, 3:66]).float().to(device)
    #pose_hand = torch.tensor(body_data['poses'][frame_num:frame_num + 1, 66:]).float().to(device)
    body_dmpls = torch.tensor(body_data['dmpls'][frame_num:frame_num + 1]).float().to(device)
    betas = torch.tensor(body_data['betas'][:10][np.newaxis]).float().to(device)
    body_img,joints = create_mesh(body= pose_body, beta= betas, dmpls= body_dmpls, root_orient= root_orient)
    return body_img,joints


def createRotationMatrix(theta):
    rot_mat = np.array([[np.cos(theta), - np.sin(theta), 0],
                        [np.sin(theta), np.cos(theta), 0],
                        [0, 0, 1]])
    return rot_mat

def createJoint(data,ax,title):
    bone_list = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [3, 6], [4, 7], [7, 10], [5, 8],
                 [6, 9], [8,11],[9,12], [9,13],[9,14], [12,15],[13, 16],[14, 17], [16, 18],
                 [14, 17], [17, 19], [19, 21], [18, 20],[21,49],[20,22]]

    xs, ys, zs = data[:, 0], data[:, 1], data[:, 2]
    ax.scatter(xs,ys,zs,s=8)
    for bone in bone_list:
        x1, x2 = xs[bone[0]], xs[bone[1]]
        y1, y2 = ys[bone[0]], ys[bone[1]]
        z1, z2 = zs[bone[0]], zs[bone[1]]
        ax.plot3D([x1, x2], [y1, y2],
                  [z1, z2], 'r', linewidth=5, zorder=1)
        ## For Labels at each point
        # for i, x, y, z in zip(range(len(xs)), xs, ys, zs):
        #     ax.text(x, y, z, i)
    ax.set_title(title)
    ax.view_init(azim=-52 , elev=13)
    #plt.show()
    return ax



def showBodyMeshOnly(body_hand_mesh,ax):
    # ax.set_aspect('auto')
    imw, imh = 1600, 1600
    mv = MeshViewer(width=imw, height=imh)
    mv.set_static_meshes([body_hand_mesh])
    body_hand_image = mv.render(render_wireframe=False)
    img = body_hand_image.astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ax.imshow(img)
    # ax.view_init(-90,90)

    return ax