#!/usr/bin/env python3
# This file is covered by the LICENSE file in the root of this project.
# Developed by: Xieyuanli Chen
# Brief: clean the LiDAR scans using our LiDAR-based moving object segmentation method

import os
import sys
import yaml
import numpy as np
from tqdm import tqdm
import argparse

from kitti_utils import load_vertex, load_labels, load_files


def get_args():
	parser = argparse.ArgumentParser("./scan_cleaner.py")
	parser.add_argument(
		'--dataset', '-d',
		type=str,
		required=True,
		help='Dataset without cleaning. No Default',
	)
	parser.add_argument(
		'--label', '-l',
		type=str,
		required=True,
		help='Label path. No Default',
	)
	parser.add_argument(
		'--sequence', '-s',
		type=str,
		required=True,
		help='Sequence number. No Default',
	)
	return parser

if __name__ == '__main__':
	parser = get_args()
	FLAGS, unparsed = parser.parse_known_args()

	print("  Dataset", FLAGS.dataset)
	print("  Label", FLAGS.label)
	print("  Sequence", FLAGS.sequence)

	# create output folder
	seqs = [FLAGS.sequence]
	if not os.path.exists(os.path.join(FLAGS.dataset, "sequences", FLAGS.sequence, "clean_scans")):
		os.makedirs(os.path.join(FLAGS.dataset, "sequences", FLAGS.sequence, "clean_scans"))

	

	for seq in seqs:
		# load moving object segmentation files
		mos_pred_seq_path = os.path.join(FLAGS.label, "sequences", seq, "predictions")
		mos_pred_files = load_files(mos_pred_seq_path)

		# load semantic segmentation files
		raw_scan_path = os.path.join(FLAGS.dataset, "sequences", seq, "velodyne")
		raw_scan_files = load_files(raw_scan_path)

		print('processing seq:', seq)

		for frame_idx in tqdm(range(len(mos_pred_files))):
			# mos_pred should be 9/251 for static/dynamic
			mos_pred, _ = load_labels(mos_pred_files[frame_idx])
			current_scan = load_vertex(raw_scan_files[frame_idx])

			clean_scan = current_scan[mos_pred < 250]
			np.array(clean_scan, dtype=np.float32).tofile(os.path.join(
				FLAGS.dataset, "sequences", seq, "clean_scans", str(frame_idx).zfill(6) + '.bin'))
