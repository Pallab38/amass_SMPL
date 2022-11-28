# Packages
1. pyrender
2. trimesh
3. cv2 
4. numpy

# Data
1. Camera Data
2. Meshes
3. Images 

# Run 
```
python pyrender_singleCam.py --frames 0 50
```
# Result 
![overlaySmpl_gtImage](000000.png)

# Multi(Interpolated) Cameras

## Camera Parameters
### 1. Naive Rasterizer
#### In camera class, **Wrong Cs**
```
self.pos = np.squeeze(-R @ tvec)
```

| ![cam1_18_wrongCs_t_0_010.png](images_diffCamConf/cam1_18_wrongCs_t_0_010.png)| ![cam1_18_wrongCs_t-0_5_010.png](images_diffCamConf/cam1_18_wrongCs_t-0_5_010.png)   |
|:--:|:--: |
| <b> cam1_18_wrongCs_t_0_010</b>|  <b>cam1_18_wrongCs_t-0_5_010.png</b>  |

|![cam1_18_wrongCs_t+1_010.png](images_diffCamConf/cam1_18_wrongCs_t+1_010.png)|  ![cam1_18_wrongCs_t-1_010.png](images_diffCamConf/cam1_18_wrongCs_t-1_010.png)|
|:--:|:--: |
| <b>cam1_18_wrongCs_t+1_010 </b>  |  <b>cam1_18_wrongCs_t-1_010</b>   |

### In camera class, **right Cs**
```
self.pos = np.squeeze(-np.transpose(R) @ tvec)
```



### 2. Pyrender
Camera Set Up 
```
camera = pyrender.camera.IntrinsicsCamera(fx=K1[0,0],fy=K1[1,1],
                                           cx=K1[0,2], cy=K1[1,2])
```
#### 2.1 (f_x, f_y)
It **does not** do the zoom in and zoom out. It just make the shape of the mesh bigger or smaller.
|![000000_fx.png](pyrender_diffConf/000000_fx.png)|  ![000000_fx150.png](pyrender_diffConf/000000_fx150.png)|
|:--:|:--: |
| <b>with original fx </b>  |  <b>Original fx increased by 50%</b>   |
