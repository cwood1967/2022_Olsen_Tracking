import pims
import pendulum
from matplotlib import pyplot as plt
import tifffile
import numpy as np
import os
from tqdm import tqdm

root_dir = '/n/core/micro/nro/lo2296/rla/aquatics'
# surface_vid = '2019-09-15_Surface/2019-09-14 12-00-00.mkv'
# cave_vid = '2019-09-05_Pachon/2019-09-05 12-00-00.mkv'
tinaja_vid = '2020-01-01/2020-01-07 12-00-00.mkv'
video_path = os.path.join(root_dir, tinaja_vid)
save_path = os.path.join(root_dir, '2020-01-01/tiff_clips/')
os.makedirs(save_path, exist_ok=True)

vid = pims.Video(video_path)

# Manually currated event times
surface_times = [
    '12:01:19',
    '12:01:20',
    '12:01:31',
    '12:01:32',
    '12:01:37',
    '12:01:38',
    '12:01:39',
    '12:01:40',
    '12:01:42',
    '12:01:43',
    '12:02:05',
    '13:28:55',
    '13:29:03',
    '13:29:05', 
    '13:29:08',
    '14:18:34',
    '14:19:04',
    '14:19:05',
    '14:32:09',
    '14:32:11',
]
cave_times = [
    '12:00:04',
	'12:00:18',
	'12:00:27',
	'12:09:12',
	'12:09:21',
	'12:10:04',
	'12:10:11',
	'12:25:25',
	'12:25:31',
	'12:25:55',
	'12:46:52',
	'12:47:31',
	'12:48:11',
	'13:07:15',
	'13:08:30',
	'13:08:41',
	'13:08:49',
	'13:36:50',
	'13:07:31',
	'14:00:13',
]
tinaja_times = [
    '12:00:15',
    '12:00:25',
    '12:01:11',
    '12:01:29',
    '12:01:32',
    '12:01:44',
    '12:01:59',
    '12:02:03',
    '12:02:17',
    '12:02:32',
    '12:04:18',
    '12:04:46',
    '12:04:50',
    '12:07:46',
    '12:09:14',
    '12:09:28',
    '12:12:20',
    '12:14:35',
    '14:40:10',
    '14:40:37',
    '14:42:58',
    '14:52:41', 
]
times = tinaja_times
frames = []
# video starts at noon
start = pendulum.from_format('12:00:00', 'HH:mm:ss')
# Convert times to frame numbers
for t in times:
    ftime = pendulum.from_format(t, 'HH:mm:ss')
    frame = (ftime - start).in_seconds()*30
    frames.append(frame)

# Save each as a tiff stack
for f in tqdm(frames):
    stack = vid[f-60:f+60]
    stack = np.array(stack)
    file_name = os.path.join(save_path, f'tinaja_{f}.tif')
    tifffile.imsave(file_name, stack)