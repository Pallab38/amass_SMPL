"""
Source : https://github.com/zju3dv/EasyMocap/blob/master/easymocap/visualize/pyrender_wrapper.py
"""
import os 
import numpy as np 
import matplotlib.pyplot as plt 
import trimesh
import pyrender
from os.path import join
from pathlib import Path
import cv2
import argparse

from MyCamera import MyCamera


if __name__=="__main__":
    data_root = "/home/pallab/thesis/sampleDataZjuMocap/subject_313"
    cam_dir = join(data_root,"camera")
    image_dir = join(data_root,"frame" )
    mesh_dir = join(data_root, "50_meshes")
    uv_fpath = join(data_root, "uv_table.npy")
    save_dir = "smpl/pyrende_singleCam"
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", nargs="+", type=int, help="Number of frames")
    args = parser.parse_args()
    frames = [i for i in range(args.frames[0], args.frames[1])]
    
    cam_num1 = 1
    all_cameras = MyCamera.load_cam_data(cam_dir)
    my_cam1 = MyCamera(all_cameras, cam_num1)
    rvec1, tvec1, K1, dist1 = my_cam1.param_for_nara()## (3,1), (3,1), (3,3),(5,1)
    print(tvec1.shape, K1.shape)
    R = cv2.Rodrigues(rvec1)[0]
    rot = trimesh.transformations.rotation_matrix(np.radians(180),[1,0,0])
    camera_pose = np.eye(4)
    camera = pyrender.camera.IntrinsicsCamera(fx=K1[0,0],fy=K1[1,1],
                                          cx=K1[0,2], cy=K1[1,2])
    bg_color=[0.0, 0.0, 0.0, 0.0]
    ambient_light=[0.5, 0.5, 0.5]
   
    for frame_num in frames:
        gt_img_fpath = join(image_dir,str(cam_num1), "%06d.jpg"%frame_num)
        mesh_fpath = join(mesh_dir,"%06d.obj"%frame_num)
        print(os.path.isfile(gt_img_fpath), gt_img_fpath)
        print(os.path.isfile(mesh_fpath))
        gt_img = cv2.cvtColor(cv2.imread(gt_img_fpath), cv2.COLOR_BGR2RGB)
        mesh = trimesh.load(mesh_fpath)
        V, F = mesh.vertices, mesh.faces
        V = V@R.T + tvec1.T
        vertex_colors = np.ones([V.shape[0],4])
        mesh1 = trimesh.Trimesh(V,F,vertex_colors=vertex_colors, process=False)
        mesh1 = mesh1.apply_transform(rot)
        my_mesh = pyrender.Mesh.from_trimesh(mesh1)
        
        r = pyrender.OffscreenRenderer(1024, 1024)
        scene = pyrender.Scene(bg_color=bg_color, ambient_light=ambient_light)
        scene.add(camera, pose= camera_pose)
        scene.add(my_mesh)
        img, depth = r.render(scene)

        save_fpath = join(save_dir,"%06d.png"%frame_num)
        fig=plt.figure(figsize=(6,6))
        ax1 = fig.add_subplot(111)
        ax1.set_xlim(0,1024)
        ax1.set_ylim(1024,0)
        ax1.imshow(gt_img)
        ax1.imshow(img, alpha=0.80)
        ax1.axis("off")
        plt.tight_layout()
        fig.savefig(save_fpath, bbox_inches="tight", pad_inches=0)
        # plt.show()
        plt.close()
        r.delete()
