import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

file1 = "Hospital1.txt"
file2 = "Hospital2.txt"

try:
    data1 = pd.read_csv(file1)
    print("Yah yee the file loaded successfully!\n")
    print(data1.head())
except FileNotFoundError:
    print(f"Error: '{file1}' not found. Check the filename and path.")
except Exception as e:
    print("An error occurred while reading the file:", e)

num_readmitted = data1[" Readmission"].sum()

avg_staff = data1[" StaffSatisfaction"].mean()
avg_clean = data1[" CleanlinessSatisfaction"].mean()
avg_food = data1[" FoodSatisfaction"].mean()
avg_comfort = data1[" ComfortSatisfaction"].mean()
avg_comm = data1[" CommunicationSatisfaction"].mean()

print("-- Patient Satisfaction Summary --")
print(f"Number of Patients Readmitted: {num_readmitted}")
print(f"Average Staff Satisfaction: {avg_staff:.2f}")
print(f"Average Cleanliness Satisfaction {avg_clean:.2f}")
print(f"Average Food Satisfaction: {avg_food:.2f}")
print(f"Average Comfort Satisfaction: {avg_comfort:.2f}")
print(f"Average Communication Satisfaction: {avg_comm:.2f}")

try:
    data2 = pd.read_csv(file2)
    print("Yah yee the file loaded successfully!\n")
    print(data1.head())
except FileNotFoundError:
    print(f"Error: '{file2}' not found. Check the filename and path.")
except Exception as e:
    print("An error occurred while reading the file:", e)

num_readmitted2 = data2[" Readmission"].sum()

avg_staff2 = data2[" StaffSatisfaction"].mean()
avg_clean2 = data2[" CleanlinessSatisfaction"].mean()
avg_food2 = data2[" FoodSatisfaction"].mean()
avg_comfort2 = data2[" ComfortSatisfaction"].mean()
avg_comm2 = data2[" CommunicationSatisfaction"].mean()

print("-- Patient Satisfaction Summary --")
print(f"Number of Patients Readmitted: {num_readmitted2}")
print(f"Average Staff Satisfaction: {avg_staff2:.2f}")
print(f"Average Cleanliness Satisfaction {avg_clean2:.2f}")
print(f"Average Food Satisfaction: {avg_food2:.2f}")
print(f"Average Comfort Satisfaction: {avg_comfort2:.2f}")
print(f"Average Communication Satisfaction: {avg_comm2:.2f}")


satisfaction_columns = [
    " StaffSatisfaction"," CleanlinessSatisfaction"," FoodSatisfaction",
    " ComfortSatisfaction"," CommunicationSatisfaction"
    ]
data1["OverallSatisfaction"] = data1[satisfaction_columns].mean(axis=1)
print(data1[["PatientID","OverallSatisfaction"," Readmission"]].head())


X1 = data1[["OverallSatisfaction"]].values
y1 = data1[" Readmission"].values

scaler1 = StandardScaler()
X_scaled1 = scaler1.fit_transform(X1)

log_reg1 = LogisticRegression()
log_reg1.fit(X_scaled1,y1)

coef = log_reg1.coef_[0][0]
intercept = log_reg1.intercept_[0]

print("-- Logistic Regression Coefficeints --")
print(f"Intercept: {intercept:.3f}")
print(f"Coefficient for Overall Satisfaction: {coef:.3f}")

if coef < 0:
    direction = "Higher satisfaction is associated with LOWER probability of readmission."
elif coef > 0:
    direction = "Higher satisfaction is associated with HIGHER probability of readmission."
else:
    direction = "No apparaent association between satisfaction and readmission."

print("\nInterpretation:")
print(direction)


x_range1 = np.linspace(data1["OverallSatisfaction"].min(),data1["OverallSatisfaction"].max(),100).reshape(-1,1)
x_range_scaled1 = scaler1.transform(x_range1)
y_prob1 = log_reg1.predict_proba(x_range_scaled1)[:,1]

plt.figure(figsize=(8,5))
plt.scatter(data1["OverallSatisfaction"],data1[" Readmission"],label="Observed Data", alpha=0.7)
plt.plot(x_range1, y_prob1,label="Logistic Regression Curve",linewidth=2)

plt.xlabel("Overall Satisfaction")
plt.ylabel("Probability of Readmission (1 = Yes)")
plt.title("Logistic Regression: Readmission vs Overall Satisfaction")
plt.legend()
plt.grid(True)
plt.show()


y_pred1 = log_reg1.predict(X_scaled1)
print("-- Classification Report --")
print(classification_report(y1,y_pred1,zero_division=0))
print("-- Confusion Matrix --")
print(confusion_matrix(y1,y_pred1))


satisfaction_columns = [
    " StaffSatisfaction"," CleanlinessSatisfaction"," FoodSatisfaction",
    " ComfortSatisfaction"," CommunicationSatisfaction"
    ]
data2["OverallSatisfaction"] = data2[satisfaction_columns].mean(axis=1)
print(data2[["PatientID","OverallSatisfaction"," Readmission"]].head())


X2 = data2[["OverallSatisfaction"]].values
y2 = data2[" Readmission"].values

scaler2 = StandardScaler()
X_scaled2 = scaler2.fit_transform(X2)

log_reg2 = LogisticRegression()
log_reg2.fit(X_scaled2,y2)

coef2 = log_reg2.coef_[0][0]
intercept2 = log_reg2.intercept_[0]

print("-- Logistic Regression Coefficeints --")
print(f"Intercept: {intercept:.3f}")
print(f"Coefficient for Overall Satisfaction: {coef:.3f}")

if coef < 0:
    direction = "Higher satisfaction is associated with LOWER probability of readmission."
elif coef > 0:
    direction = "Higher satisfaction is associated with HIGHER probability of readmission."
else:
    direction = "No apparaent association between satisfaction and readmission."

print("\nInterpretation:")
print(direction)


x_range2 = np.linspace(data2["OverallSatisfaction"].min(),data2["OverallSatisfaction"].max(),100).reshape(-1,1)
x_range_scaled2 = scaler2.transform(x_range2)
y_prob2 = log_reg2.predict_proba(x_range_scaled2)[:,1]

plt.figure(figsize=(8,5))
plt.scatter(data2["OverallSatisfaction"],data2[" Readmission"],label="Observed Data", alpha=0.7)
plt.plot(x_range2, y_prob2,label="Logistic Regression Curve",linewidth=2)

plt.xlabel("Overall Satisfaction")
plt.ylabel("Probability of Readmission (1 = Yes)")
plt.title("Logistic Regression: Readmission vs Overall Satisfaction")
plt.legend()
plt.grid(True)
plt.show()


y_pred2 = log_reg2.predict(X_scaled2)
print("-- Classification Report --")
print(classification_report(y2,y_pred2,zero_division=0))
print("-- Confusion Matrix --")
print(confusion_matrix(y2,y_pred2))