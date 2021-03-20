import csv
import numpy as np  
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from datetime import datetime

# Prepares wildfire data, AQI data for processing
# Insert your path of corresponding datasets here 
wildfire_data = pd.read_csv('/Users/andrew/Dropbox/My Mac (Andrew’s MacBook Pro (2))/Downloads/ProjectGreenify/Data-Analysis/ca-wildfires-weather/ca-wildfire-statistics.csv')
aqi_data = pd.read_csv('/Users/andrew/Dropbox/My Mac (Andrew’s MacBook Pro (2))/Downloads/ProjectGreenify/Data-Analysis/ca-wildfires-weather/ca-2020-weekly-aqi.csv')

# Converts AQI data from CSV to numpy format and saves as .npy file
aqi_np_data = np.genfromtxt('/Users/andrew/Dropbox/My Mac (Andrew’s MacBook Pro (2))/Downloads/ProjectGreenify/Data-Analysis/ca-wildfires-weather/ca-2020-weekly-aqi.csv', delimiter=",", usecols=np.arange(0, 53));
np.savetxt('aqi.npy', aqi_np_data, delimiter=',')

aqi_dates_list = [] # List storing weekly AQI testing dates

with open('/Users/andrew/Dropbox/My Mac (Andrew’s MacBook Pro (2))/Downloads/ProjectGreenify/Data-Analysis/ca-wildfires-weather/ca-2020-weekly-aqi.csv', newline='') as f:
    # Reads top row of weekly AQI measurement days and adds to aqi_dates_list
    reader = csv.reader(f)
    for row in reader:
        aqi_dates_list.append(row)
        break
    aqi_dates_list[0].pop(0)


def find_date(fire_name):
    '''
        Returns start date and end date for specified fire

        Parameters:
                fire_name (str): String representation of fire to find start
                                 and containment dates for (e.g. "August Complex")
        Returns:
                start_date (datetime): Datetime object representing start date
                                       in %m/%y format of fire specified
                end_Date (datetime): Datetime object representing end (containment)
                                     date in %m/%y format of fire specified
    '''
    index = -1

    # Finding index of specified fire
    for i in range (0, wildfire_data.shape[0]):
        if (fire_name==wildfire_data['Name'][i]):
            index = i

    # Assigns and prints start, containment dates for specified fires
    start_date = datetime.strptime(str(wildfire_data['Start Date'][index]), "%m/%d")
    end_date = datetime.strptime(str(wildfire_data['Containment Date'][index]), "%m/%d")
    # Replace year 1900 with 2020 in datetime format
    start_date = start_date.replace(year=2020).date()
    end_date = end_date.replace(year=2020).date()

    return start_date, end_date


def get_ranked_fires(rank):
    '''
    Returns name of specified fire rank by acres burnt (greatest->least) as string.

        Parameters:
                rank (int): Positive, nonzero integer which determines rank of fire
                            (e.g. 1=1st, 2=2nd, 3=3rd)

        Returns:
                fire_name (str): String of fire name at specified rank
                                 (e.g. "SCU Lightning Complex")
            
    '''
    acres_list = [ ]
    fire_name = "NULL"
    acres_max = 0

    # Loads dataset into list 
    for i in range(0, wildfire_data.shape[0]):
        acres_list.append(wildfire_data['Acres'][i])

    # Finds specified fire by rank of most acres burnt 
    for i in range (0, rank): 
        acres_max = max(acres_list) # Finds max 
        max_index = acres_list.index(acres_max) 
        acres_list[max_index] = -1 # Replaces max with sentinel value to skip over for 2nd, 3rd, etc
        fire_name = wildfire_data['Name'][max_index] 

    return fire_name


def display_aqi_plot(aqi_np_data, title):
    '''
        Displays plot of AQI (measured in PM2.5 and/or Ozone) vs time
        with corresponding axes, titles labeled.

        Parameters:
                aqi_np_data (numpy array): Numpy array storing 
                                           weekly PM2.5/Ozone AQI data
                title (str): String representation of Title of graph
                             (excluding "AQI vs Time")
    '''
    x_dates = [datetime.strptime(str(d), '%m/%d/%Y').date() for d in aqi_dates_list[0]]
    y_aqi = np.delete(aqi_np_data, 0)

    fig = plt.figure()
    plt.plot(x_dates, y_aqi)
    fig.suptitle(title + ' AQI vs Time')
    plt.xlabel('Time')
    plt.ylabel('AQI Levels (PM2.5/Ozone)')
    fig.savefig(title + '.jpg')


def display_all(number_of_top_fires):
    '''
    Displays all weekly AQI data on single plot.
    
    Parameters:
            number_of_top_fires (int): Positive, nonzero integer representing number
                                       of top fires to generate markers for
    '''
    x_dates = [datetime.strptime(str(d), '%m/%d/%Y').date() for d in aqi_dates_list[0]]
    fig = plt.figure()
    for i in range(1, 8):
        plt.plot(x_dates, np.delete(aqi_np_data[i], 0), linewidth=0.5)
    display_fire_markers(number_of_top_fires)
    fig.suptitle('All Fires AQI vs Time')
    plt.xlabel('Time')
    plt.ylabel('AQI Levels (PM2.5/Ozone)')
    fig.savefig('AllFires.jpg')
    plt.show()


def display_fire_markers(number_of_top_fires):
    '''
    Displays vertical dotted-line markers indicating start and end times
    of largest fires; generates color-coded legend for each fire marker

    Parameters:
            number_of_top_fires (int): Positive, nonzero integer representing number
                                       of top fires to generate markers for
    '''
    fire_index = 1
    fire_coords = [ find_date(get_ranked_fires(i)) for i in range (1, number_of_top_fires) ]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    for fc,c in zip(fire_coords, colors):
        plt.axvline(x=fc[0], c=c, linestyle='dashed', alpha=0.5)
        plt.axvline(x=fc[1], label='{}'.format(get_ranked_fires(fire_index)), c=c, linestyle='dashed', alpha=0.5)
        fire_index += 1
    plt.legend()

# Displays all plots on a single figure with top 5 largest fires start & end dates marked
display_all(5) 

# Currently CSV has data on 7 Bay Area locations listed below
# Uncomment each to generate corresponding plots
#display_aqi_plot(aqi_np_data[1], 'SFO-Arkansas St')
#display_aqi_plot(aqi_np_data[2], 'San Ramon')
#display_aqi_plot(aqi_np_data[3], 'Pleasanton-Owens Ct')
#display_aqi_plot(aqi_np_data[4], 'Hayward')
#display_aqi_plot(aqi_np_data[5], 'San Jose-Jackson St')
#display_aqi_plot(aqi_np_data[6], 'San Jose-Knox Ave')
#display_aqi_plot(aqi_np_data[7], 'Redwood City')
#plt.show()
