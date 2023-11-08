import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('DSP Project Midterms - Sheet1.csv')

standard_deviation = df.std().astype(int)
variance = df.var().astype(int)

standard_deviation = standard_deviation.round(2)
variance = variance.round(2)

print("Standard Deviation:\n", standard_deviation.to_string(), "\n")
print("Variance:\n", variance.to_string(), "\n")

central_tendency = pd.DataFrame({'Standard Deviation': standard_deviation, 'Variance': variance})
central_tendency.plot(kind='bar', legend=True)

plt.title('Variability of the Two-week Meteorological Data')
plt.xlabel('Statistics')
plt.ylabel('Values')

plt.show()