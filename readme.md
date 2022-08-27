# Overview

## Prerequisite
1. smplx (``` pip install smplx ```)  [PyPi Project (pip)](https://pypi.org/project/smplx/)
2. pyrender (```pip install pyrender```)   [PyPi Project (pip)](https://pypi.org/project/pyrender/)
3. trimesh (```pip install trimesh```)  [PyPi Project (pip)](https://pypi.org/project/trimesh/)
## We need 
a) **Vertices** (6890,3)  ```/home/group-cvg/cvg-students/das1/zju_mocap/CoreView_313/new_vertices/1.npy``` <br>
b) **Joints**  (24,3) <br>
c) **Pose** (1,num_jointsx3=72) ```/home/group-cvg/cvg-students/das1/zju_mocap/CoreView_313/new_params/1.npy```<br>
## Code
```
from smplx import SMPL  ### pip install smplx

###  Load SMPL Model    ### 
smpl = SMPL(model_path= <path to Gender.pkl file>, gender="MALE")

```
