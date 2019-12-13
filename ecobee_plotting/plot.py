import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import glob
import re
from datetime import datetime

# written by Jordan Wheeler on 9-13-2019
# written on mac for my thermostat unsure about compadabililty with other operating systems and thermostats
# but i tried to make it pretty general


night_pm = 20 #what time does it get dark
night_am = 7  #what time does it get light

#grab the file
csv_files = glob.glob("*.csv")
filename = csv_files[0]

#Read in the data
ncols = np.genfromtxt(filename,delimiter = ",",skip_header = 6).shape[1] # how many columns
input_dtypes = ["<U10","<U10","<U10","<U10","<U10","<U10"] # first six are strings
for i in range(len(input_dtypes),ncols): # the rest are floats
    input_dtypes.append("<f8")

data = np.genfromtxt(filename,delimiter = ",",
                         dtype = input_dtypes,
                         names = True,missing_values = "",filling_values = np.nan,skip_header = 5,usecols = np.arange(0,ncols-1))

# convert time to array that is usable for plotting
time_arr = np.zeros(len(data['Date'])) # initialzie the array
night = np.zeros(len(data['Date']))
for i in range(0,len(data['Date'])):
    string = data['Date'][i] + " "+ data['Time'][i]
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', string)
    date_and_time= datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
    time_arr[i] = matplotlib.dates.date2num(date_and_time)
    if int(date_and_time.strftime('%H')) >night_pm: # its late
        night[i] = 1
    if int(date_and_time.strftime('%H')) <night_am: # its early
        night[i] = 1

night_index = np.where(night>0.5)
day_index = np.where(night<0.5)




#plot all temperatures

# find data indexes that contain temperatures
temp_indexes = []
for i in range(0,len(data.dtype.names)):
    if "_F" in data.dtype.names[i]: temp_indexes.append(i)

        
fig, ax = plt.subplots(figsize= (12,6))
ax.set_title('Click on legend line to toggle line on/off')

plot_dict = {} #initalize a dictionary to hold all of our matplotlib lines

# plot the lines
count = 0
for i in temp_indexes:
    plot_dict["line"+str(count)] = ax.plot(time_arr,data[data.dtype.names[i]],label = data.dtype.names[i],linewidth = 2)
    count = count +1

# make the legend
leg = ax.legend(loc='upper left', fancybox=True, shadow=False,ncol = 2)
leg.get_frame().set_alpha(0.4)


# we will set up a dict mapping legend line to orig line, and enable
# picking on the legend line

# put lines in a list
lines = []
for i in range(0,len(plot_dict.keys())):
    lines.append(plot_dict['line'+str(i)][0])
    
lined = dict()
for legline, origline in zip(leg.get_lines(), lines):
    legline.set_picker(5)  # 5 pts tolerance
    lined[legline] = origline


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
plt.xticks(rotation=10,ha="right")
plt.ylabel("Temperature (F)")
plt.xlabel("Date and time")
ylim = ax.get_ylim()
night_ylim = night*ax.get_ylim()[1]
night_ylim[day_index] = ax.get_ylim()[0]

ax.fill_between(time_arr,np.ones(len(time_arr))*ax.get_ylim()[0],night_ylim,color = 'grey',alpha = 0.2)
ax.set_ylim(ylim)


def onpick(event):
    # on the pick event, find the orig line corresponding to the
    # legend proxy line, and toggle the visibility
    legline = event.artist
    origline = lined[legline]
    vis = not origline.get_visible()
    origline.set_visible(vis)
    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled
    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.2)
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', onpick)

# plot the humidity
plt.figure(2, figsize = (12,6))
plt.plot(time_arr,data["Thermostat_Humidity_RH"],label = "Thermostat_Humidity_RH",color = "C1",linewidth = 2)
plt.ylabel("Relative Humidity (%)")
plt.xlabel("Date and time")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
plt.xticks(rotation=10,ha="right")

plt.show()


