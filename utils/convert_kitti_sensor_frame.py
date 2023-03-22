import numpy as np
import os
import sys
from tqdm import tqdm
import argparse
import pypcd
import open3d as o3d

def get_args():
    parser = argparse.ArgumentParser("./convert_scania_sensor_frame.py")
    parser.add_argument(
        '--scanpath', '-s',
        type=str,
        required=True,
        help='Path of the scania sensor frame scan'
    )
    parser.add_argument(
        '--posepath', '-p',
        type=str,
        required=True,
        help='Path of the scania pose'
    )
    parser.add_argument(
        '--outputpath', '-o',
        type=str,
        required=True,
        help='Path of output'
    )
    return parser

def transform_poses(scan_path, pose_path, output_path):
    try:
        if not (os.path.isdir(output_path+'converted/')):
            os.makedirs(output_path+'converted/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            print ("Failed to create directory!!!!!")
            raise
    
    if '.bin' in scan_path:
        points = np.fromfile(scan_path, dtype=np.float32)
        split_list = scan_path.split('/')
        split_list = split_list[-1].split('.')
        id = int(split_list[0])
        pcd_file_name = "{:06d}.pcd".format(id)
        with open(pose_path, 'r') as f:
            lines = f.readlines()
            print(len(lines ))
            points = points.reshape((-1, 4))[:, 0:3]
            points = np.transpose(points)
            np_ones = np.ones((1, points.shape[1]))
            points = np.vstack((points, np_ones))
            transform = np.fromstring(lines[id], dtype=float, sep=' ')
            transform = transform.reshape(3, 4)
            transform = np.vstack((transform, [0, 0, 0, 1]))
            points = np.matmul(transform, points)
            points = np.transpose(points)[:, 0:3]
            o3d_pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
            o3d.io.write_point_cloud(output_path+'converted/'+pcd_file_name, o3d_pcd)  
            f.close()
    else:
        pcd_files = []
        for (path, dir, files) in os.walk(scan_path):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == '.bin':
                    pcd_files.append(path + "/" + filename)
        pcd_files.sort()  
        with open(pose_path, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                points = np.fromfile(pcd_files[i], dtype=np.float32)
                pcd_file_name = "{:06d}.pcd".format(i)
                points = points.reshape((-1, 4))[:, 0:3]
                points = np.transpose(points)
                np_ones = np.ones((1, points.shape[1]))
                points = np.vstack((points, np_ones))
                transform = np.fromstring(lines[i], dtype=float, sep=' ')
                transform = transform.reshape(3, 4)
                transform = np.vstack((transform, [0, 0, 0, 1]))
                points = np.matmul(transform, points)
                points = np.transpose(points)[:, 0:3]
                o3d_pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
                o3d.io.write_point_cloud(output_path+'converted/'+pcd_file_name, o3d_pcd)  
            f.close()




if __name__ == '__main__':
    parser = get_args()
    FLAGS, unparesed = parser.parse_known_args()
    
    print("  Scan Path", FLAGS.scanpath)
    print("  Pose Path", FLAGS.posepath)
    print("  Output Path", FLAGS.outputpath)
    transform_poses(FLAGS.scanpath, FLAGS.posepath, FLAGS.outputpath)
