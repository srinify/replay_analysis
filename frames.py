import cv2
import numpy as np
import os

# split_frames() reads from /pfs/videos and outputs results to /pfs/out.
# /pfs/.. are special folders in pachyderm filesystem
def split_frames(video_file):
	print(video_file)
	cap = cv2.VideoCapture(video_file)

	if(cap.isOpened() == False):
		print("Error opening video file")

	# E.g. Extract 'first_video' from 'pfs/videos/first_video.mp4'
	# for naming the output folder
	video_file_name = os.path.split(video_file)
	
	frames_dir = video_file_name[1].split('.')[0]
	pach_frames_dir = "/pfs/out/" + frames_dir
	os.mkdir(pach_frames_dir)

	print(pach_frames_dir)

	current_frame = 0
	
	# Keep going until loop breaks, when there's no frames left
	while(True):
		# This loop iteration returned a frame
		ret, frame = cap.read()

		# No frames left, it's quitting time!
		if not ret:
			break

		# Write out each frame: frame1.jpg, frame2.jpg, etc.
		image_name = pach_frames_dir + '/frame' + str(current_frame) + '.jpg'
		write_status = cv2.imwrite(image_name, frame)
		if write_status is True:
			print(image_name + ' successfully written')
		current_frame += 1
		print(current_frame)

	# Releases the I/O
	cap.release()


# Walk /pfs/videos and call split_frames() on each file
for dirpath, dirs, files in os.walk("/pfs/videos"):
	print(dirpath)
	print(files)
	for file in files:
		if file.endswith('mp4'):
			split_frames(os.path.join(dirpath, file))