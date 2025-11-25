import pandas as pd
#from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt


# Parameters
TheCsvInQuestion = "HillsboroughCoFL_DistToHurricaneShelters_x120_a250000m2_1764089128.077461.csv"
percentile_specificity = 100
plt.figure(figsize=(15,10))


distances = list()
df = pd.read_csv(TheCsvInQuestion,header=0)

for index, row in df.iterrows():
    distances.append(row["Distance"])
    #line_distance = ufloat(row["Distance"],row["uDist"])
    #print(line_distance)

percentiles_to_calc = np.linspace(0, 100, percentile_specificity+1)
dist_percentiles = np.percentile(distances,percentiles_to_calc)
plt.plot(np.array(percentiles_to_calc),np.array(dist_percentiles),label=TheCsvInQuestion)
plt.title("Percentiles of the Distances from land locations throughout Hillsborough County, FL.")
plt.xlabel("Percentile")
plt.ylabel("Distance (miles)")
plt.legend()
plt.show()