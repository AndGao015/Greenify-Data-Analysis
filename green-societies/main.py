import csv
import time
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure 
from datetime import datetime
from operator import itemgetter

# Greenhouse gas emissions measured in tonnes of CO2 equivalent, in thousands
# And list of all countries in dataset
ghg_df = pd.read_csv('AIR_GHG_25042021055804023.csv')

# Depletion and growth of forest resources in terms of volume
# Measured in cubic metres, thousands
forest_df = pd.read_csv('FOREST_25042021060647140.csv')

# Generation of waste by sector, total waste per capita
waste_df = pd.read_csv('WSECTOR_26042021030408107.csv')

# Environmental tax revenue by country
tax_df = pd.read_csv('ERTR_26042021031927071.csv')

ghg_country_list = ['Australia', 'Austria', 'Belgium', 'Canada', 'Czech Republic', 
                'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 
                'Iceland', 'Ireland', 'Italy', 'Japan', 'Korea', 'Luxembourg', 
                'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland', 'Portugal', 
                'Slovak Republic', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom', 
                'United States', 'Chile', 'Estonia', 'Israel', 'Russia', 'Slovenia', 'Latvia', 
                'Lithuania', 'Brazil', "China (People's Republic of)", 'Colombia', 'Costa Rica', 
                'India', 'Indonesia', 'South Africa', 'Argentina']

tax_country_list = ['Australia', 'Austria', 'Belgium', 'Canada', 'Czech Republic', 
                    'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 
                    'Iceland', 'Ireland', 'Italy', 'Japan', 'Korea', 'Luxembourg', 
                    'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland', 'Portugal', 
                    'Slovak Republic', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom', 
                    'United States', 'Albania', 'Argentina', 'Bahamas', 'Belize', 'Bolivia', 
                    'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 
                    'Cameroon', 'Cabo Verde', 'Chile', "China (People's Republic of)", 'Colombia', 
                    'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cyprus', 'Democratic Republic of the Congo', 
                    'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Estonia', 
                    'Fiji', 'Ghana', 'Guatemala', 'Guyana', 'Honduras', 'India', 'Indonesia', 'Israel', 
                    'Jamaica', 'Kazakhstan', 'Kenya', 'Latvia', 'Liechtenstein', 'Lithuania', 'North Macedonia', 
                    'Madagascar', 'Malaysia', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 
                    'Namibia', 'Nicaragua', 'Niger', 'Nigeria', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 
                    'Philippines', 'Romania', 'Russia', 'Rwanda', 'Samoa', 'Senegal', 'Seychelles', 'Singapore', 
                    'Slovenia', 'Solomon Islands', 'South Africa', 'Eswatini', 'Togo', 'Trinidad and Tobago', 'Tunisia', 
                    'Uganda', 'Uruguay', 'Venezuela', 'Serbia', 'Montenegro', 'Saint Lucia', 'Barbados', 'Mongolia', 
                    'Thailand', 'Malawi', 'Bhutan', 'Nauru', 'Cook Islands', 'Chad']

waste_country_list = ['Austria', 'Belgium', 'Czech Republic', 'Denmark', 'Finland', 'France', 'Germany', 
                      'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Japan', 'Korea', 'Luxembourg', 
                      'Netherlands', 'Norway', 'Poland', 'Portugal', 'Slovak Republic', 'Spain', 'Sweden', 
                      'Switzerland', 'Turkey', 'United Kingdom', 'Chile', 'Estonia', 'Latvia', 'Lithuania', 
                      'Slovenia', 'Australia', 'Colombia', 'Israel']

forest_country_list = ['Australia', 'Austria', 'Belgium', 'Canada', 'Czech Republic', 'Denmark', 'Finland', 
                       'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Japan', 'Korea', 
                       'Luxembourg', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland', 'Portugal', 'Slovak Republic', 
                       'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom', 'United States', 'Chile', 'Estonia', 'Russia', 
                       'Slovenia', 'Colombia', 'Costa Rica', 'Latvia', 'Lithuania']

overlap_country_list = list(set(set(ghg_country_list).intersection(tax_country_list)).intersection(waste_country_list))

def show_headers_and_types(df): 
    for header in df.columns:
        header = str(header)
        header_type_list = [ ]
        if ((header=='Value') or (header=='Reference Period Code')
            or (header=='Reference Period')):
            continue 

        for index, row in df.iterrows():
            if (row[header] not in header_type_list):
                header_type_list.append(row[header])

        print(f'{header}: ')
        print(header_type_list)
        print()


def plot_country_var(var_df, var1, var2, var3, country, show):
    """
        var_df: dataframe 

        var1, var2, var3: 2 element array specifying data
            1st element = header of variable
            2nd element = specific variable

        country: string representing country to find data for

        show: boolean indicating whether to display plot
            True = display plot and return nparr containing data points
            False = only return nparr containing data points
    """
    if (show):
        fig = plt.figure(figsize=(7, 7), dpi=100)    

    year_list = [ ]
    if ((len(var1)==0) and (len(var2)==0) and (len(var3)==0)):
        print('No data specified')
    elif ((len(var2)==0) and (len(var3)==0)):
        df = var_df.loc[(var_df['Country']==country) & 
            (var_df[var1[0]] == var1[1])]
    elif ((len(var2)!=0) and (len(var3)==0)):
        df = var_df.loc[(var_df['Country']==country) & 
            (var_df[var1[0]] == var1[1]) & (var_df[var2[0]] == var2[1])]
    else:
        df = var_df.loc[(var_df['Country']==country) & 
            (var_df[var1[0]] == var1[1]) & (var_df[var2[0]] == var2[1]) 
            & (var_df[var3[0]] == var3[1])]

    if (len(df)==0):
        print('No data available for specified country and variable(s)')
        print(f'{var1[0]}')
        return

    y_df = [ ]

    for index, row in df.iterrows():
        year_list.append(row['Year'])
        y_df.append(row['Value'])

    x_years = np.asarray([datetime.strptime(str(d), '%Y').date() for d in year_list])
    y_var = np.asarray(y_df)

    if (show):
        plt.plot(x_years, y_var, label=country)

        fig.suptitle(f'{var1[1]} vs Time')
        plt.xlabel('Year')
        plt.ylabel(f'{var1[1]}')

        plt.legend()
        plt.show()

    return y_var


def plot_multiple_country_var(var_df, var1, var2, var3, country_list, show):
    """
        var_df: dataframe of variable

        var1, var2, var3: 2 element array specifying data
            1st element = header of variable
            2nd element = specific variable

        country_list: list of strings representing countries to gather data for

        show: boolean indicating whether to display plot
            True = display plot and return nparr containing data points
            False = only return nparr containing data points
    """
    y_var_data = [ ]
    if (show):
        fig = plt.figure(figsize=(7, 7), dpi=100)    

    for country in country_list:
        year_list = [ ]
        if ((len(var1)==0) and (len(var2)==0) and (len(var3)==0)):
            print('No data specified')
        elif ((len(var2)==0) and (len(var3)==0)):
            df = var_df.loc[(var_df['Country']==country) & 
                (var_df[var1[0]] == var1[1])]
        elif ((len(var2)!=0) and (len(var3)==0)):
            df = var_df.loc[(var_df['Country']==country) & 
                (var_df[var1[0]] == var1[1]) & (var_df[var2[0]] == var2[1])]
        else:
            df = var_df.loc[(var_df['Country']==country) & 
                (var_df[var1[0]] == var1[1]) & (var_df[var2[0]] == var2[1]) 
                & (var_df[var3[0]] == var3[1])]

        if (len(df)==0):
            print('No data available for specified country and variable(s)')
            print(f'{var1[0]}')
            continue

        y_df = [ ]

        for index, row in df.iterrows():
            year_list.append(row['Year'])
            y_df.append(row['Value'])

        x_years = np.asarray([datetime.strptime(str(d), '%Y').date() for d in year_list])
        y_var = np.asarray(y_df)

        if (show):
            plt.plot(x_years, y_var, label=country)

        y_var_data.append(y_var)

    if (show):
        fig.suptitle(f'{var1[1]} vs Time')
        plt.xlabel('Year')
        plt.ylabel(f'{var1[1]}')

        plt.legend()
        plt.show()

    return y_var_data


def calc_plot_corr(nparr1, nparr2):
    if (len(nparr1) > len(nparr2)):
        nparr1 = nparr1[0:len(nparr2)]
        # print(f'Num data points: {len(nparr2)}')
    else:
        nparr2 = nparr2[0:len(nparr1)]
        # print(f'Num data points: {len(nparr1)}')
    
    if ((len(nparr1)>=2) and (len(nparr2)>=2)):
        plot_corr = np.corrcoef(nparr1, nparr2)
        print(f'r = {plot_corr[0][1]}')
        return plot_corr
    else:
        print('Insufficient data available')


def find_list_intersection(l1, l2):
    return list(set(l1).intersection(l2))
        

# Greenhouse gas emissions including LULUCF
# plot_country_ghg('Australia', 'TOTAL_LULU')
# plot_country_ghg('United States', 'TOTAL_LULU')
# plot_country_ghg('Iceland', 'TOTAL_LULU')
# plot_country_ghg('Mexico', 'TOTAL_LULU')
# plot_country_ghg('Netherlands', 'TOTAL_LULU')

# Pass in list of countries to plot
# plot_multiple_ghg(["China (People's Republic of)", 'India', 'Australia', 'United States', 'Iceland', 'Mexico'], 'TOTAL_LULU')

# Show headers, types for environmental tax dataframe
# show_headers_and_types(tax_df)

# Want to look @ 'Tax revenue, % of total environmentally related tax revenue'
# for i in range(0, 46, 5):
    # plot_multiple_ghg(overlap_country_list[i:i+5], 'TOTAL_LULU')
    # plot_multiple_tax(overlap_country_list[i:i+5])

# print(overlap_country_list)

"""
corr_arr = [ ]

for name in overlap_country_list:
    print(f'{name}: ')
    nparr1 = plot_country_var(waste_df, ['ISIC', 'SECWAS_CAP'], [], [], name, show=False)
    nparr2 = plot_country_var(ghg_df, ['VAR', 'TOTAL_LULU'], ['POL', 'GHG'], [], name, show=False)

    try:
        corr_arr.append(calc_plot_corr(nparr1, nparr2))
    except:
        print('Insufficient data')
        continue
    finally:
        print()
"""

# show_headers_and_types(forest_df)

l = find_list_intersection(forest_country_list, waste_country_list)
m = find_list_intersection(l, tax_country_list)
final_country_list = find_list_intersection(m, ghg_country_list)


# Plotting for each of GHG, waste, env tax, deforestation
    
    # Total emissions including LULUCF, pollutant = greenhouse gases
# plot_multiple_country_var(ghg_df, ['VAR', 'TOTAL_LULU'], ['POL', 'GHG'], [], final_country_list, show=True)

    # Total waste per capita
# plot_multiple_country_var(waste_df, ['ISIC', 'SECWAS_CAP'], [], [], final_country_list, show=True)

    # Net fellings
# plot_multiple_country_var(forest_df, ['Variable', 'Net fellings'], [], [], final_country_list, show=True)

    # Tax revenue, % of total environmentally related tax revenue
# plot_multiple_country_var(tax_df, ['VAR', 'BASE_ERTR'], ['Category', 'Pollution'], [], final_country_list, show=True)

corr_arr = [ ]


for name in final_country_list:
    print(f'{name}: ', end='')

    # Waste per capita
    nparr_waste = plot_country_var(waste_df, ['ISIC', 'SECWAS_CAP'], [], [], name, show=False)
    # Total GHG emissions including LULUCF
    nparr_ghg = plot_country_var(ghg_df, ['VAR', 'TOTAL_LULU'], ['POL', 'GHG'], [], name, show=False)
    # Net fellings
    nparr_forest = plot_country_var(forest_df, ['Variable', 'Net fellings'], [], [], name, show=False)
    # % of total tax which is environmentally related for pollution
    nparr_tax = plot_country_var(tax_df, ['VAR', 'BASE_ERTR'], ['Category', 'Pollution'], [], name, show=False)
    
    """ Correlation between two nparrs"""
    try:
        corr_arr.append(calc_plot_corr(nparr_forest, nparr_ghg))
    except:
        print('Insufficient data')
        continue
    finally:
        print()


