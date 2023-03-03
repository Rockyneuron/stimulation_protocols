import pandas as pd
import sys
import os
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot   as plt
import seaborn as sns



data_loc=Path("data/000/exports/000/annotations.csv")
data=pd.read_csv(data_loc)

time_stamps=data['index'].values

diff_time=np.diff(time_stamps)


print(diff_time)

fig1,ax1=plt.subplots(1)
sns.histplot(data=diff_time,ax= ax1, bins=20)


