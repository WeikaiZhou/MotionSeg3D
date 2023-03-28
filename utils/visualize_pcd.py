import numpy as np
import open3d as o3d

if __name__ == "__main__":

    print("Load a pcd point cloud, print it")
    pcd = o3d.io.read_point_cloud("/home/wzhoea/Desktop/removert_save/run4/map_static/StaticMapScansideMapLocal.pcd")
    print(pcd)
    print(np.asarray(pcd.points))
    o3d.visualization.draw_geometries([pcd])