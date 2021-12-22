import matplotlib.pyplot as plt
import numpy as np
import glob

from pairOfClosestFactor import calc_closest_factors

## https://stackoverflow.com/questions/51285630/draw-lines-into-skeleton-joints-coordinates-with-python-and-matplotlib
def make_skeleton(path):
    '''
    Create skeleton from given joints position without hands.
    :param path: path of directory
    :type path: str
    :return: Does not return anything shows plot
    :rtype: n/a
    '''
    ##### Bones
    bone_list = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [3, 6], [4, 7], [4, 10], [5, 8], [5, 11],
             [6, 9], [9, 13], [9, 14], [13, 12], [14, 12], [12, 15], [13, 16], [16, 18],
             [14, 17], [17, 19], [19, 21], [18, 20]
            ]
    bone_list = np.array(bone_list)

    file_list = glob.glob(path)
    # print(file_list)
    fig = plt.figure(figsize=(10,8)) #
    rows,cols = calc_closest_factors(len(file_list))
    axes = [fig.add_subplot(rows,cols, i+1,projection="3d") for i in range(len(file_list))]

    for ax,file_path in zip(axes,file_list):
        file = np.loadtxt(file_path)
        xs, ys, zs = file[:,0],file[:,1],file[:,2]
        ax.scatter(xs,ys,zs,s=2)
        for bone in bone_list:
            ax.plot3D([xs[bone[0]], xs[bone[1]]],
                    [ys[bone[0]], ys[bone[1]]],
                    [zs[bone[0]], zs[bone[1]]], 'r')
        ax.view_init(-90, 90)
        ax.set_axis_off()
    # fig.suptitle("Joints Data with Hands")
    # fig.savefig("joints_data_w_hands.jpg")
    plt.show()


if __name__=='__main__':
    dir_path = "../Data/jointData_w_hand/*.txt"
    make_skeleton(dir_path)
