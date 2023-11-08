import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('DSP Project Midterms - Sheet1.csv')

mean = df.mean()
median = df.median()
mode = df.mode().iloc[0]

print("Mean:\n", mean.to_string(),"\n")
print("Median:\n", median.to_string(), "\n")
print("Mode:\n", mode.to_string(), "\n")

central_tendency = pd.DataFrame({'Mean': mean, 'Median': median, 'Mode': mode})
central_tendency.plot(kind='bar', legend=True)

plt.title('Central Tendency of the Two-week Meteorological Data')
plt.xlabel('Statistics')
plt.ylabel('Sensor Values')

plt.show()