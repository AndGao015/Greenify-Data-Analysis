def plot_country_ghg(country_name, var_type, show):
    exclude_country_list = [ 'OECD - Total', 'OECD - Europe', 'European Union (28 countries)' ]

    country_name_list = [ ]
    year_list = [ ]
    
    for index, row in ghg_df.iterrows():
        if (((row['Country'] not in country_name_list) and (row['Country'] not in exclude_country_list))
            and (row['Year'] not in year_list)):
            country_name_list.append(row['Country'])
            year_list.append(row['Year'])

    df = ghg_df.loc[(ghg_df['Country'] == country_name) & (ghg_df['POL'] == 'GHG') & (ghg_df['VAR'] == var_type)]
    df_ghg = [ ]

    for index, row in df.iterrows():
        df_ghg.append(row['Value'])
  
    # Reassign size in order to catch out of bounds errors
    # Has to match length of df_ghg
    year_list = year_list[0:len(df_ghg)]

    x_years = np.asarray([datetime.strptime(str(d), '%Y').date() for d in year_list])
    y_ghg = np.asarray(df_ghg)

    if (show):
        fig = plt.figure(figsize=(7, 7), dpi=100)
        plt.plot(x_years, y_ghg)
        fig.suptitle(f'{country_name} Total GHG vs Time')
        plt.xlabel('Year')
        plt.ylabel('Greenhouse Gas Emissions including LULUCF')
        plt.legend()
        plt.show()

    return y_ghg


def plot_multiple_ghg(country_list, var_type):
    fig = plt.figure(figsize=(7, 7), dpi=100)
    year_list = [ ]

    for country in country_list:
        for index, row in ghg_df.iterrows():
            if (row['Year'] not in year_list):
                year_list.append(row['Year'])

        df = ghg_df.loc[(ghg_df['Country'] == country) & (ghg_df['POL'] == 'GHG') & (ghg_df['VAR'] == var_type)]
        df_ghg = [ ]

        for index, row in df.iterrows():
            df_ghg.append(row['Value'])
  
        # Reassign size in order to catch out of bounds errors
        # Has to match length of df_ghg
        year_list = year_list[0:len(df_ghg)]

        x_years = np.asarray([datetime.strptime(str(d), '%Y').date() for d in year_list])
        y_ghg = np.asarray(df_ghg)

        plt.plot(x_years, y_ghg, linewidth = 0.5, label=country)

    country_str = ' '
    for i in range (0, len(country_list)):
        if (i==len(country_list)-2):
            country_str += country
        else:
            country_str += country + ', '

    fig.suptitle(f'Total GHG vs Time')
    plt.xlabel('Year')
    plt.ylabel('Greenhouse Gas Emissions including LULUCF')
    plt.legend()

    plt.show()


def plot_average_ghg():
    ghg_averages = [ ]

    for country_name in country_name_list:
        df = ghg_df.loc[(ghg_df['Country'] == country_name) & (ghg_df['POL'] == 'GHG') & (ghg_df['VAR'] == 'TOTAL_LULU')]
        if (str(df['Value'].mean()) == 'nan'):
            avg = 0
        else:
            avg = df['Value'].mean()
        ghg_averages.append((country_name, int(avg)))

    ghg_avg_vals = [ ]

    for country_name, average in ghg_averages:
        print(f"{country_name}: {average}")
        ghg_avg_vals.append(average)
    
    df = pd.DataFrame({'GHG Emissions': ghg_avg_vals}, index = country_name_list)
    fig = df.plot.bar(rot=90, figsize=(14, 7))
    fig.set_xticklabels(country_name_list, fontsize=8)
    plt.subplots_adjust(bottom=.254)
    plt.legend()

    plt.show()


def plot_country_tax(country, show):
    exclude_country_list = ['OECD Asia Oceania', 'OECD America', 'OECD arithmetic average']
    if (show):
        fig = plt.figure(figsize=(7, 7), dpi=100)    

    year_list = [ ]
    df = tax_df.loc[(tax_df['Country'] == country) & (tax_df['CAT'] == 'ENE') & (tax_df['VAR'] == 'BASE_ERTR')
                    & (tax_df['DOM'] == 'CC')]
    df_tax = [ ]

    for index, row in df.iterrows():
        year_list.append(row['Year'])
        df_tax.append(row['Value'])

    x_years = np.asarray([datetime.strptime(str(d), '%Y').date() for d in year_list])
    y_tax = np.asarray(df_tax)
    
    if (show):
        plt.plot(x_years, y_tax, label=country)

        fig.suptitle(f'Percent Environmental Tax Revenue vs Time')
        plt.xlabel('Year')
        plt.ylabel('Percent of total tax revenue related to environmental taxes')

        plt.legend()
        plt.show()

    return y_tax



def plot_multiple_tax(country_list):
    exclude_country_list = ['OECD Asia Oceania', 'OECD America', 'OECD arithmetic average']
    country_name_list = [ ]
    fig = plt.figure(figsize=(7, 7), dpi=100)    

    for index, row in tax_df.iterrows():
        if ((row['Country'] not in country_name_list) and (row['Country'] not in exclude_country_list)):
            country_name_list.append(row['Country'])

    for country in country_list:
        year_list = [ ]
        df = tax_df.loc[(tax_df['Country'] == country) & (tax_df['CAT'] == 'ENE') & (tax_df['VAR'] == 'BASE_ERTR')
                        & (tax_df['DOM'] == 'CC')]
        df_tax = [ ]

        for index, row in df.iterrows():
            year_list.append(row['Year'])
            df_tax.append(row['Value'])

        x_years = np.asarray([datetime.strptime(str(d), '%Y').date() for d in year_list])
        y_tax = np.asarray(df_tax)

        plt.plot(x_years, y_tax, label=country)

    fig.suptitle(f'Percent Environmental Tax Revenue vs Time')
    plt.xlabel('Year')
    plt.ylabel('Percent of total tax revenue related to environmental taxes')
    plt.legend()

    plt.show()

