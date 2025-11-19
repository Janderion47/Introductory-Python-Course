import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

file_path = "Week14Assignment.txt"

try:
    data = pd.read_csv(file_path)
    print("Yah yee the file loaded successfully!\n")
    print(data.head())
except FileNotFoundError:
    print(f"Error: '{file_path}' not found. Check the filename and path.")
except Exception as e:
    print("An error occurred while reading the file:", e)

num_readmitted = data[" Readmission"].sum()

avg_staff = data[" StaffSatisfaction"].mean()
avg_clean = data[" CleanlinessSatisfaction"].mean()
avg_food = data[" FoodSatisfaction"].mean()
avg_comfort = data[" ComfortSatisfaction"].mean()
avg_comm = data[" CommunicationSatisfaction"].mean()

print("-- Patient Satisfaction Summary --")
print(f"Number of Patients Readmitted: {num_readmitted}")
print(f"Average Staff Satisfaction: {avg_staff:.2f}")
print(f"Average Cleanliness Satisfaction {avg_clean:.2f}")
print(f"Average Food Satisfaction: {avg_food:.2f}")
print(f"Average Comfort Satisfaction: {avg_comfort:.2f}")
print(f"Average Communication Satisfaction: {avg_comm:.2f}")

satisfaction_columns = [
    " StaffSatisfaction"," CleanlinessSatisfaction"," FoodSatisfaction",
    " ComfortSatisfaction"," CommunicationSatisfaction"
    ]
data["OverallSatisfaction"] = data[satisfaction_columns].mean(axis=1)
print(data[["PatientID","OverallSatisfaction"," Readmission"]].head())


X = data[["OverallSatisfaction"]].values
y = data[" Readmission"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

log_reg = LogisticRegression()
log_reg.fit(X_scaled,y)

coef = log_reg.coef_[0][0]
intercept = log_reg.intercept_[0]

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


x_range = np.linspace(data["OverallSatisfaction"].min(),data["OverallSatisfaction"].max(),100).reshape(-1,1)
x_range_scaled = scaler.transform(x_range)
y_prob = log_reg.predict_proba(x_range_scaled)[:,1]

plt.figure(figsize=(8,5))
plt.scatter(data["OverallSatisfaction"],data[" Readmission"],label="Observed Data", alpha=0.7)
plt.plot(x_range, y_prob,label="Logistic Regression Curve",linewidth=2)

plt.xlabel("Overall Satisfaction")
plt.ylabel("Probability of Readmission (1 = Yes)")
plt.title("Logistic Regression: Readmission vs Overall Satisfaction")
plt.legend()
plt.grid(True)
plt.show()


y_pred = log_reg.predict(X_scaled)
print("-- Classification Report --")
print(classification_report(y,y_pred,zero_division=0))
print("-- Confusion Matrix --")
print(confusion_matrix(y,y_pred))