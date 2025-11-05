import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = {

    'Age': [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],

    'BloodPressure': [120, 122, 126, 128, 130, 133, 135, 138, 142, 145, 150, 155, 160, 165, 170, 175]

}

df = pd.DataFrame(data)
df.head()

print("Shape (rows, columns):", df.shape)
print("\nColumn types:")
print(df.dtypes)
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nSummary statistics:")
print(df.describe())

plt.figure(figsize=(7,5))
plt.scatter(df['Age'],df['BloodPressure'],label='Patient Data')

x = df[['Age']]
y = df[['BloodPressure']]
model = LinearRegression()
model.fit(x,y)
slope = model.coef_[0][0]
intercept = model.intercept_[0]
print(f"Regression Equation: Blood Pressure = {slope:.4f} * Age + {intercept:.4f}")

y_hat = model.predict(x)
plt.plot(df['Age'],y_hat, label= 'Regression Line')

plt.xlabel("Age (years)")
plt.ylabel("Blood Pressure (mmHg)")
plt.title("Age vs Blood Pressure - Scatter Plot, with Linear Regression Fit - Age -> Blood Pressure")
plt.grid(True)
plt.legend()
plt.show()

example_ages = [[30], [40], [50], [60]]
predicted_bp = model.predict(example_ages)

for (age,), bp in zip(example_ages,predicted_bp):
    print(f"Predicted Blood Pressure at Age {age}: {bp[0]:.2f} mmHg")