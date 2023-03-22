import numpy as np
import os
import sys
from tqdm import tqdm
import argparse

def get_args():
    parser = argparse.ArgumentParser("./convert_scania_pose.py")
    parser.add_argument(
        '--posepath', '-p',
        type=str,
        required=True,
        help='Path of the scania pose'
    )
    return parser

def transform_poses(pose_path):
    if '.txt' in pose_path:
        with open(pose_path, 'r') as f:
            with open(os.path.abspath(pose_path + '/..') + '/poses.txt', 'w') as s:
                lines = f.readlines()
                transform_matrix = np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]])
                for line in lines:
                    current = np.fromstring(line, dtype=float, sep=' ')
                    current = current[1::].reshape(3, 4)
                    transformed = np.matmul(transform_matrix, current[0:3, 0:3])
                    current[0:3, 0:3] = transformed
                    new_col = np.array([[-current[1, 3]], [-current[2, 3]], [current[0, 3]]])
                    current[0, 3] = new_col[0, 0]
                    current[1, 3] = new_col[1, 0]
                    current[2, 3] = new_col[2, 0]
                    flat_arr = current.flatten()
                    s.write(' '.join(map(str, flat_arr)))
                    s.write('\n')
                s.close()
            f.close()

if __name__ == '__main__':
    parser = get_args()
    FLAGS, unparesed = parser.parse_known_args()
    
    print("  Pose Path", FLAGS.posepath)
    transform_poses(FLAGS.posepath)
