import numpy as np
import open3d as o3d

if __name__ == "__main__":

    print("Load a pcd point cloud, print it")
    pcd = o3d.io.read_point_cloud("/home/wzhoea/Desktop/scania_dataset/sequences/00/ssps_FL/008409.pcd")
    print(pcd)
    print(np.asarray(pcd.points))
    o3d.visualization.draw_geometries([pcd])