import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data=pd.read_csv('pupil_positions.csv')


ratio_frames=np.diff(data['pupil_timestamp'].values)

plt.hist(ratio_frames)