import pandas as pd

data = pd.read_csv("Week13Assignment.txt")

age_avg = data[" Age"].mean()

male = 0
female=0
for gender in data[" Gender"]:
    if gender == "male":
        male += 1
    elif gender=="female":
        female += 1

systolic = list()
diastolic= list()
for bp in data[" BloodPressure"]:
    sys, dia = bp.split("/")
    systolic.append(int(sys))
    diastolic.append(int(dia))

systolic_avg = sum(systolic)/len(systolic)
diastolic_avg= sum(diastolic)/len(diastolic)

temp_avg = data[" Temperature"].mean()


print("-- Patients' Data Statistics --")
print(f"The average age of the patients is {age_avg}.")
print(f"The number of male and female patients is {male} and {female} respectively.")
print(f"The blood pressures have an average systolic pressure of {systolic_avg} and average diastolic pressure of {diastolic_avg}.")
print(f"The highest and lowest systolic pressures are {max(systolic)} and {min(systolic)}.")
print(f"The highest and lowest diastolic pressures are {max(diastolic)} and {min(diastolic)}.")
print(f"The average patient temperature is {temp_avg} celsius.")