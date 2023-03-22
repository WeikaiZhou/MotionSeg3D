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
    try:
        if '.txt' in pose_path:
            with open(pose_path, 'r') as f:
                with open(os.path.abspath(pose_path + '/..') + '/poses.txt', 'w') as s:
                    lines = f.readlines()
                    base = np.fromstring(lines[0], dtype=float, sep=' ')
                    base = base[1::].reshape(3, 4)
                    base = np.vstack((base, [0, 0, 0, 1]))
                    s.write('1 0 0 0 0 1 0 0 0 0 1 0')
                    s.write('\n')
                    for i in range(1, len(lines)):
                        current = np.fromstring(lines[i], dtype=float, sep=' ')
                        current = current[1::].reshape(3, 4)
                        current = np.vstack((current, [0, 0, 0, 1]))
                        current = np.matmul(base, np.linalg.inv(current))
                        current = current[0:3, :]
                        flat_arr = current.flatten()
                        s.write(' '.join(map(str, flat_arr)))
                        s.write('\n')
                    s.close()
                f.close()


    except FileNotFoundError:
        print('No file avaiable')

if __name__ == '__main__':
    parser = get_args()
    FLAGS, unparesed = parser.parse_known_args()
    
    print("  Pose Path", FLAGS.posepath)
    transform_poses(FLAGS.posepath)
