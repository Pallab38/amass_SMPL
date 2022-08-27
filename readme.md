# Overview

## Prerequisite
1. smplx (``` pip install smplx ```)  [PyPi Project (pip)](https://pypi.org/project/smplx/)
2. pyrender (```pip install pyrender```)   [PyPi Project (pip)](https://pypi.org/project/pyrender/)
3. trimesh (```pip install trimesh```)  [PyPi Project (pip)](https://pypi.org/project/trimesh/)
## We need 
a) **Vertices** (6890,3)  <br>
b) **Joints**  (24,3) <br>
c) **Pose** (1,num_jointsx3=72) <br>
## Code
```
from smplx import SMPL  ### pip install smplx

###  Load SMPL Model    ### 
smpl = SMPL(model_path= <path to Gender.pkl file>, gender="MALE")

```
