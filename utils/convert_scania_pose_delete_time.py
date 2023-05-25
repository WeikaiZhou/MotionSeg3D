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
                    with open(os.path.abspath(pose_path + '/..') + '/times.txt', 'w') as t:
                        lines = f.readlines()
                        for line in lines:
                            split_string = line.split(' ')
                            s.write(' '.join(split_string[2::]))
                            t.write(split_string[1] + '\n')
                        s.close()
                        t.close()
                f.close()


    except FileNotFoundError:
        print('No file avaiable')

if __name__ == '__main__':
    parser = get_args()
    FLAGS, unparesed = parser.parse_known_args()
    
    print("  Pose Path", FLAGS.posepath)
    transform_poses(FLAGS.posepath)
