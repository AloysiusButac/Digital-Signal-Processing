import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime, timedelta

class Datapoint:
    date = datetime(2023, 10, 19, 12, 0, 0, 0)
    humi = -1
    temp = -1

    def __init__(self, _date, _humi, _temp):
        self.date = _date
        self.humi = _humi
        self.temp = _temp

## unused function
def insert_interval(arr, interval, ave_1=None, ave_2=None):
    total_filled = 0
    total_mins_filled = 0
    # if type(arr[0]) is Datapoint:
    #     arr = [ a.date for a in arr ]
    filled_arr = []
    filled_i = 0

    for i in range(len(arr)-1):
        # First encounter
        if len(filled_arr) <= 0:
            filled_arr.append(arr[i])

        while (arr[i+1].date - filled_arr[filled_i].date) > interval:
            if arr[i+1].date.minute() < filled_arr[filled_i].date.minute() + interval:
                filled_arr.append(Datapoint(arr[i+1].date, arr[i+1].humi, arr[i+1].temp))
            else:
                if ave_1 is None:
                    ave_1 = (arr[i+1].humi + filled_arr[filled_i].humi) // 2
                if ave_2 is None:
                    ave_2 = (arr[i+1].temp + filled_arr[filled_i].temp) // 2

                filled_arr.append(Datapoint(filled_arr[filled_i].date + interval, ave_1, ave_2))
                total_filled += 1
                total_mins_filled += interval.total_seconds() / 60
            filled_i += 1
        
        if arr[i+1].date < filled_arr[filled_i].date + interval:
            filled_arr.append(Datapoint(arr[i+1].date, arr[i+1].humi, arr[i+1].temp))
            filled_i += 1

    print("Total Filled data:", total_filled, "(", total_filled/4, "hrs ) ")
    print("Total Time Filled :", total_mins_filled, "(", total_mins_filled/60, "hrs ) ")

    return filled_arr

rows = []
datapoints = []
date_format = '%m/%d/%Y_%H:%M:%S'

# Import data from file
with open("DSP Project Midterms - Sheet1.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
        dp_date = Datapoint(datetime.strptime(row[0],date_format), float(row[1]), float(row[2]))
        datapoints.append(dp_date)

start = 0
count = len(rows)
humi_ave = temp_ave = interval_ave = 0
max_interval = 15
min_interval = 15
missing_mins = 0
time_jumps = 0

# Proccessing data (1)
for i in range(start+1, count):
    # Time interval between datapoints
    interval = (datapoints[i].date - datapoints[i-1].date).seconds / 60
    # Check for large/small intervals
    if int(interval) > 15:
        bad_int = '%.3f'%(interval)
        missing_mins += interval
        bad_int_hrs = '%.3f'%(interval/60)
        print("Bad interval at:", i+1, " - interval:", bad_int, "\t(", bad_int_hrs, "hrs )", datapoints[i-1].date.strftime("%H:%M:%S"), datapoints[i].date.strftime("%H:%M:%S"))

    # # Print data
    # print(
    #     i+1,
    #     datapoints[i-1].date, datapoints[i-1].humi, 
    #     datapoints[i-1].temp, "\tinterval:", interval
    #     )

    humi_ave += datapoints[i-1].humi
    temp_ave += datapoints[i-1].temp
    interval_ave += interval

# Calculating averages
humi_ave /= (count - start)
temp_ave /= (count - start)
interval_ave /= (count - start)

# inserted_data = insert_interval(datapoints[start:count], timedelta(seconds=900))
inserted_data = datapoints
collection_period = datapoints[len(datapoints)-1].date - datapoints[0].date

print()
print("len:", len(datapoints))
print("Ave_humi:", humi_ave, "Ave_temp:", temp_ave)
print("Ave_inter:", interval_ave, "mins")
print("Total missing hours:", '%.3f'%(missing_mins / 60))
print("Total Data Collection period: ", datapoints[0].date.strftime("%m/%d - %H:%M:%S"), "-", datapoints[len(datapoints)-1].date.strftime("%m/%d - %H:%M:%S"), "(",collection_period.total_seconds()/3600,"hrs )")

print()

# with open("output.csv", "w", encoding="UTF8", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(['DATE', 'HUMIDITY', 'TEMPERATURE'])
#     for data in inserted_data:
#         writer.writerow([data.date.strftime('%m/%d/%Y_%H:%M:%S'), data.humi, data.temp])

# Display graph
interval = len(inserted_data)-1
date_first = inserted_data[0].date
date_last = inserted_data[interval].date

nums = [ a for a in range(interval)]

humi = [ data.humi for data in inserted_data ]
temp = [ data.temp for data in inserted_data ]

# date_label = [ data.date.strftime("%m/%d_%H:%M") for data in inserted_data ]
date_label = []
date_holder = [ date.date for date in inserted_data ]

holder = inserted_data[0].date.strftime("%m/%d_%H:%M")
for i in range(interval):
    if i % (interval//10) == 0:
        holder = inserted_data[i].date.strftime("%M/%d_%H:%M")
    date_label.append(holder)

print("Holder len:", len(date_label))

plt.title("DHT11 Sensor Humidity and Temperature Data")
plt.subplot(211)
plt.plot(date_holder[0:interval], humi[0:interval])
plt.grid()

## Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M')) 
# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=20)) 
# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)  
# Changes x-axis range
plt.gca().set_xbound(date_first, date_last) 
plt.ylabel("Humidity")

plt.subplot(212)
plt.plot(date_holder[0:interval], temp[0:interval])
plt.grid()

## Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M')) 
# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=20)) 
# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)  
# Changes x-axis range
plt.gca().set_xbound(date_first, date_last) 
plt.ylabel("Temperature")

plt.show()