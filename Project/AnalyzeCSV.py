import pandas as pd
#from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt
from math import ceil


# Parameters
TheCsvInQuestion = "HillsboroughCoFL_DistToHurricaneShelters_x120_a250000m2_1764089128.077461.csv"
percentile_spec = 100
plt.figure(figsize=(15,10))


distances = list()
df = pd.read_csv(TheCsvInQuestion,header=0)

for index, row in df.iterrows():
    distances.append(row["Distance"])
    #line_distance = ufloat(row["Distance"],row["uDist"])
    #print(line_distance)

thepercentiles = np.linspace(0, 100, percentile_spec+1)
thepercentiles_major = np.linspace(0, 100, 4+1)
percent_data = np.percentile(distances,thepercentiles)
percent_major_data = np.percentile(distances,thepercentiles_major)
plt.plot(np.array(thepercentiles),np.array(percent_data),label=TheCsvInQuestion)
plt.scatter(np.array(thepercentiles_major),np.array(percent_major_data),label="0th, 25th, 50th, 75th, and 100th percentiles")
plt.title("Percentiles of the Distances from land locations throughout Hillsborough County, FL.")
plt.xlabel("Percentile")
plt.ylabel("Distance (miles)")
plt.legend()
plt.show()

print("0th percentile:",percent_data[0])
print("25th percentile:", percent_data[ceil(percentile_spec*0.25)])
print("50th percentile:", percent_data[ceil(percentile_spec*0.50)])
print("75th percentile:", percent_data[ceil(percentile_spec*0.75)])
print("100th percentile:", percent_data[ceil(percentile_spec)])