import numpy as np  
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from datetime import datetime

codata = pd.read_csv('/Users/andrew/Dropbox/My Mac (Andrew’s MacBook Pro (2))/Downloads/ProjectGreenify/Data-Analysis/alameda-covid-co/alameda_2020_co_emissions.csv', parse_dates=['Date'], dayfirst=False)

def next_month(i):
    if (i==12):
        return 1
    else:
        return i+1

def get_averages(site_name):
    index = 0
    while True:
        temp = codata['Site Name'][index]
        if (temp != site_name):
            index += 1
        else:
            print(index)
            while True:
                nine_month_averages = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                counter = index
                daily = datetime.strptime(str(codata['Date'][0]), "%Y-%m-%d %H:%M:%S")

                for i in range(1, 10):
                    days_in_month = 0
                    average = 0
                    month_start = datetime(2020, i, 1)
                    month_end = datetime(2020, next_month(i), 1)

                    while True:
                        if ((daily >= month_start) and (daily < month_end)):
                            average += codata['Daily Max 8-hour CO Concentration'][counter]
                            counter += 1
                            days_in_month += 1
                            daily = datetime.strptime(str(codata['Date'][counter]), "%Y-%m-%d %H:%M:%S")
                        else:
                            break
                    nine_month_averages[i-1] = average/days_in_month

                print(f"{site_name} CO Averages from Jan-Sept: ")
                for avg in nine_month_averages:
                    print(f"{avg:.4f}")

                break
            break

print('Sites: Oakland, Oakland West, Laney College, Berkeley Aquatic Park, Pleasanton - Owens Ct')
site = input('Enter site to analyze: ')

get_averages(site)
