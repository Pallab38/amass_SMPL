import os
from pathlib import Path
import numpy as np


# =========         Create Randomly Sampled Path of Dataset files           =============
def create_sample_file(bodyData_dir,num_of_file,file_name):
    bodydata_dir = bodyData_dir  #  "../Data/bodyData"
    all_file_paths = []
    for dirEntry in os.scandir(bodydata_dir):
        if dirEntry.is_dir(): ## Dataset -> BMLhandball
            # print("dirEntry.path: ",dirEntry.path)
            # print("dirEntry.name: ",dirEntry.name)
            for d in os.scandir(dirEntry): ## Inside the dataset; type of action -> S01_Expert
                if d.is_dir():
                    # print("d.path: ",d.path)
                    # print("d.name: ",d.name)
                    file_path = [files.path for files in os.scandir(d) if files.is_file()]
                    file_path = file_path[1:]
                    # print("len(file_path): ",len(file_path))
                    # print("file_path: ",file_path)
                    if(len(file_path)>num_of_file-1):
                        all_file_paths.append(file_path)

    print("len(all_file_paths): ",len(all_file_paths))
    # print("all_file_paths[0]: ",all_file_paths[0])
    print("len(all_file_paths[0]): ",len(all_file_paths[0]))
    choosen_files = []
    for type_act in all_file_paths:
        single_length = len(type_act)
        count = np.random.randint(0,single_length,num_of_file)
        for i in count:
            choosen_files.append(type_act[i])
    print(choosen_files)

    # Write the file paths in a txt file

    # with open("filePathToVisualize.txt","w") as output:
    with open(file_name,"w") as output:
        for single_path in choosen_files:
            output.write(str(single_path) +'\n')
    print("file writing done")




######## Load the file  [to check] ###

def load_sample_file(file_name,num_of_file):
    file_txt =Path(file_name).read_text()  ## Path("filePathToVisualize.txt").read_text()
    lines = file_txt.splitlines()
    print("len(lines): ",len(lines))
    ## Take num_of_file=5 or 6 files for each type for visualization
    for i in range(0,len(lines)-num_of_file,num_of_file):
        print("iteration count: ", i)
        for j in range(i,i+5):
            single_file_path = lines[j]
            # print("single file count: ",j)
            # print(single_file_path)
            # print(type(single_file_path))

            extract_path = os.path.split(single_file_path)[0]
            dataset_p = extract_path.split("\\")[1]
            print(dataset_p)
            dir_name = os.path.split(extract_path)[-1]
            print(dir_name)
            # print(dir_name)
            # print(type(dir_name))


            # load_data = np.load(single_file_path)
            # print(load_data)

if __name__ =='__main__':
    bodyData_dir  =  "../Data/bodyData"
    file_name = "filePathToVisualize.txt"
    num_of_file = 6

    # create_sample_file(bodyData_dir,num_of_file,file_name)
    load_sample_file(file_name,num_of_file)