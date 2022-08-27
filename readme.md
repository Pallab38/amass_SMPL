# Overview

## Prerequisite
1. smplx (``` pip install smplx ```)  [Pypi project](https://pypi.org/project/smplx/)

## We need 
a) **Vertices** (6890,3)  <br>
b) **Joints** <br>
c) **Pose** (24,3) <br>
## Code
```
from smplx import SMPL  ### pip install smplx

###  Load SMPL Model    ### 
smpl = SMPL(model_path= <path to Gender.pkl file>, gender="MALE")

```
