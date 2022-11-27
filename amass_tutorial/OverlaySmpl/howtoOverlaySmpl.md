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
In camera class
```
self.pos = np.squeeze(-np.transpose(R) @ tvec)
```

| ![cam1_18_wrongCs_t+1_010.png](images_diffCamConf/cam1_18_wrongCs_t+1_010.png) | ![cam1_18_wrongCs_t_0_010.png](images_diffCamConf/cam1_18_wrongCs_t_0_010.png)| 
|:--:|:--: |
| <b>cam1_18_wrongCs_t+1_010.png</b>| <b> cam1_18_wrongCs_t_0_010.png</b>|
