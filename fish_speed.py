import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from read_roi import read_roi_zip
import math as m


pixel_scale = 27.5 # pixels per centimeter
d_scale = 1/27.5  # centimeters per pixel
fps = 30  # frames per second
t_scale = 1/fps  # seconds
roi_dir = 'path/to/rois'
save_path = os.path.join(roi_dir,'data.csv')
# roi_file = 'surface_2370.zip'

df = pd.DataFrame(columns=['name', 'v_max (cm/s)', 'v_avg (cm/s)', 'data',])


for root, dirs, files in os.walk(roi_dir):
    files = [f for f in files if f.endswith('.zip')]
    files.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))
    for roi_file in files:
        if roi_file.endswith('.zip'):
            roi_path = os.path.join(roi_dir,roi_file)
            rois = read_roi_zip(roi_path)

            points = []
            for i, roi in rois.items():
                point = {}
                point['x'] = roi['x'][0]
                point['y'] = roi['y'][0]
                point['f'] = roi['position']
                points.append(point)

            # Make sure points are correctly ordered in time
            points.sort(key=lambda x: x['f'])
            v_list = []
            max_v = 0
            for i in range(len(points)):
                if i == 0:
                    continue
                # Measure from the previous point
                p0 = points[i-1]
                p1 = points[i]
                distance = m.sqrt((p1['x'] - p0['x'])**2 + (p1['y'] - p0['y'])**2) * d_scale
                time = abs(p1['f'] - p0['f']) * t_scale
                velocity = distance / time
                points[i]['d'] = distance
                points[i]['t'] = time
                points[i]['v'] = velocity
                v_list.append(velocity)
                if velocity > max_v:
                    max_v = velocity
            avg_v = np.array(v_list).sum() / len(v_list)

            df = df.append({'name':roi_file, 'v_max (cm/s)': max_v, 'v_avg (cm/s)': avg_v, 'data': points,}, ignore_index=True)

print(df)
df.to_csv(save_path)
