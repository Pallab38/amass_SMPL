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

import open3d as o3
#### Show Image  ###
from tools import show_image

### To Rotate Global Orientation
from human_body_prior.tools.omni_tools import apply_mesh_tranfsormations_


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

## https://gist.github.com/iansan5653/1e306da9688d85934385b266e74f153a
def calc_closest_factors(c: int):
    """Calculate the closest two factors of c.

    Returns:
      [int, int]: The two factors of c that are closest; in other words, the
        closest two integers for which a*b=c. If c is a perfect square, the
        result will be [sqrt(c), sqrt(c)]; if c is a prime number, the result
        will be [1, c]. The first number will always be the smallest, if they
        are not equal.
    """
    if c // 1 != c:
        raise TypeError("c must be an integer.")

    a, b, i = 1, c, 0
    while a < b:
        i += 1
        if c % i == 0:
            a = i
            b = c // a

    return [b, a]

def show_image(img_ndarray,joints, title):
    '''
    :param img_ndarray: Nx400x400x3
    '''
    img = img_ndarray.astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    height_inch = 8
    width_inch = height_inch*(w/h)
    fig = plt.figure(figsize=(width_inch,height_inch))
    ax = fig.add_subplot(111,projection="3d")
    ax.imshow(img,aspect='auto')
    fig.canvas.draw()

    ##### Bones
    bone_list = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [3, 6], [4, 7], [4, 10], [5, 8], [5, 11],
                 [6, 9], [9, 13], [9, 14], [13, 12], [14, 12], [12, 15], [13, 16], [16, 18],
                 [14, 17], [17, 19], [19, 21], [18, 20]
                 ]
    bone_list = np.array(bone_list)
    xs, ys, zs = joints[:,0], joints[:,1],joints[:,2]
    ax.scatter(xs,ys,zs)
    fig.canvas.draw()
    for bone in bone_list:
        ax.plot3D([xs[bone[0]], xs[bone[1]]],
                [ys[bone[0]], ys[bone[1]]],#'r')
                [zs[bone[0]], zs[bone[1]]],'r')
    fig.canvas.draw()
    ax.set_title(title)
    plt.tight_layout()

    plt.axis('off')

    # fig.canvas.draw()
    # return True

def body_model():
    body_model_path = r"C:\Users\shunn0\Desktop\THESIS\TASK01\code\amass_tutorial\Data\bodyModels\smplh\male\model.npz"
    dmpl_path = r"C:\Users\shunn0\Desktop\THESIS\TASK01\code\amass_tutorial\Data\bodyModels\dmpl\male\model.npz"
    num_betas = 10
    num_dmpls = 8
    bm = BodyModel(bm_path=body_model_path, num_betas=num_betas, num_dmpls=num_dmpls, path_dmpl=dmpl_path)

    return bm

def create_mesh(body,  beta=torch.zeros((1,8)).to(device), dmpls=torch.zeros((1,3)).to(device),
                root_orient=torch.zeros((1,3)).to(device), hand=torch.zeros((1,90)).to(device),create_joints=False):
    ## Mesh Viewer Set up
    imw, imh = 1600, 1600
    mv = MeshViewer(width=imw, height=imh)
    bm = body_model()
    face = c2c(bm.f)  ## np.array(13776,3) from torch.Tensor([13776, 3]# )
    body = bm(pose_body=body, pose_hand=hand, betas=beta, dmpls=dmpls, root_orient=root_orient)
    num_vertices = body.v[0].shape[0]

    body_mesh = trimesh.Trimesh(vertices=c2c(body.v[0]), faces=face,
                                vertex_colors=np.tile(colors['grey'], (num_vertices, 1)),
                                process=False)

    if (create_joints == True):
        joint_data = c2c(body.Jtr[0])  # (52, 3)
        ### Save joints data in a txt file
        # np.savetxt(txtFileName,joint_data)
        joint_mesh = points_to_spheres(joint_data, vc=colors['red'], radius=0.005)
        apply_mesh_tranfsormations_(([body_mesh] + joint_mesh), trimesh.transformations.rotation_matrix(120, (0, 0, 1)))
        apply_mesh_tranfsormations_(([body_mesh] + joint_mesh), trimesh.transformations.rotation_matrix(30, (1, 0, 0)))
        mv.set_static_meshes(([body_mesh] + joint_mesh))
        body_img = mv.render(render_wireframe=True)
        # return body_img,joint_mesh

        return body_mesh,joint_data,joint_mesh
    else:
        apply_mesh_tranfsormations_([body_mesh], trimesh.transformations.rotation_matrix(120, (0, 0, 1)))
        apply_mesh_tranfsormations_([body_mesh], trimesh.transformations.rotation_matrix(30, (1, 0, 0)))
        mv.set_static_meshes([body_mesh])
        body_img = mv.render(render_wireframe=False)
        return body_img

def extractData_createImg(body_data,with_joints):
    frame_num =1
    root_orient = torch.Tensor(body_data['poses'][frame_num:frame_num + 1, :3]).float().to(device)
    pose_body = torch.tensor(body_data['poses'][frame_num:frame_num + 1, 3:66]).float().to(device)
    #pose_hand = torch.tensor(body_data['poses'][frame_num:frame_num + 1, 66:]).float().to(device)
    body_dmpls = torch.tensor(body_data['dmpls'][frame_num:frame_num + 1]).float().to(device)
    betas = torch.tensor(body_data['betas'][:10][np.newaxis]).float().to(device)

    if(with_joints==True):
        body_img,joints,j_mesh = create_mesh(body= pose_body, beta= betas, dmpls= body_dmpls, root_orient= root_orient, create_joints= True)
        return body_img,joints,j_mesh
    else:
        body_img = create_mesh(body= pose_body, beta=betas, dmpls=body_dmpls, root_orient=root_orient,create_joints=False)
        return body_img


def plotting_cv2(body_img, joints):
    img = body_img.astype(np.uint8)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #cv2.imshow("Body Image ", img)

    ##### Bones
    bone_list = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [3, 6], [4, 7], [4, 10], [5, 8], [5, 11],
                 [6, 9], [9, 13], [9, 14], [13, 12], [14, 12], [12, 15], [13, 16], [16, 18],
                 [14, 17], [17, 19], [19, 21], [18, 20]
                 ]
    bone_list = np.array(bone_list)
    xs, ys, zs = joints[:, 0], joints[:, 1], joints[:, 2]
    for bone in bone_list:
        x1 = int(xs[bone[0]])
        x2 = int(xs[bone[1]])
        y1 = int(ys[bone[0]])
        y2 = int(ys[bone[1]])
        cv2.line(img,(x1, y1 ),(x2 ,y2),(0,255,0),3)
                  #[zs[bone[0]], zs[bone[1]]], 'r')
    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

































