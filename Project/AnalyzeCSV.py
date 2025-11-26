import pandas as pd
#from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt


# Parameters
TheCsvInQuestion = "HillsboroughCoFL_DistToHurricaneShelters_x120_a250000m2_1764089128.077461.csv"
percentile_spec = 500
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
z = []
for i in range(5):
    val = f"{int(i*25)}th percentile: {percent_major_data[i]}"
    z.append(val)

for i,txt in enumerate(z):
    imax_x = 1
    imax_y = 1
    if i == 4:
        imax_x = 0.75
        imax_y = 0.9
    plt.text(thepercentiles_major[i]*imax_x,percent_major_data[i]*imax_y,txt)
    print(txt)
plt.scatter(np.array(thepercentiles_major),np.array(percent_major_data),label="0th, 25th, 50th, 75th, and 100th percentiles")
plt.title("Percentiles of the Distances from land locations throughout Hillsborough County, FL.")
plt.xlabel("Percentile")
plt.ylabel("Distance (miles)")
plt.legend()
plt.show()

print("Summary of the data")
print(f"From the file: {TheCsvInQuestion}")
print("0th percentile:",percent_major_data[0])
print("25th percentile:", percent_major_data[1])
print("50th percentile:", percent_major_data[2])
print("75th percentile:", percent_major_data[3])
print("100th percentile:", percent_major_data[4])