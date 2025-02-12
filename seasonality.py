#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:42:22 2024

@author: Ruyao (Anthony) Tian – Boston Crime DS2500 Project
"""
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append("/Users/showhq/Desktop/DS2500")

FILENAME = '/Users/showhq/Desktop/DS2500/data/crime2023.csv'

# Q1 Functions – chunking data into months + finding most freq. crimes per month
def clean_crime_df(df):
    '''Clean crime dataset(s). For crime trends over time analysis, dropping
    irrelevant rows, then ensures offense_description is all str's.'''
    df = df.drop(['INCIDENT_NUMBER', 'OFFENSE_CODE', 'OFFENSE_CODE_GROUP', 
                 'DISTRICT', 'REPORTING_AREA', 'UCR_PART', 'Lat', 'Long', 
                 'Location'], axis=1).copy()
    df['OFFENSE_DESCRIPTION'] = df['OFFENSE_DESCRIPTION'].astype(str).str.strip()
    return df

def filter_out_2024(df, year=2024):
    '''Filters out inputted year; default is 2024'''
    filtered_df = df[df['YEAR'] != year]
    return filtered_df

def month_separator(df):
    '''Separates dataset into 12 datasets based on months. Returns a dict where
    keys are month numbers; values are the corresponding smaller datasets'''
    month_dfs = {}
    for month in range(1, 13):
        month_data = df[df['MONTH'] == month]
        month_dfs[month] = month_data.copy()
    return month_dfs

def month_accessor(monthly_dfs, month_input):
    '''Takes in a dictionary of month dataframes, and a desired month, returns
    the dataframe for that month'''
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    if isinstance(month_input, str):
        month_number = months.index(month_input) + 1
    month_df = monthly_dfs.get(month_number)
    print(f"Crime data for {month_input}:")
    return month_df

def crime_counter(df):
    '''Takes a crime_df. Counts occurrences of each crime in offense_description
    column. Returns a dictionary–– crimes as keys; crime frequencies as values'''
    crime_counts = {}
    for crime in df['OFFENSE_DESCRIPTION']:
        if crime in crime_counts:
            crime_counts[crime] += 1
        else:
            crime_counts[crime] = 1 
    return crime_counts

def most_frequent_crimes(monthly_dfs, amt=3, display=True):
    '''Takes in a dict of monthly_dfs. Returns dict w/ durations (months/seasons)
    as keys; top 3 most frequent crimes as values. Optional: amt of top crimes
    shown, default is 3; display gives option to print output, default is True'''
    top_crimes_by_month = {}
    for month, df in monthly_dfs.items():
        crime_counts = crime_counter(df)
        sorted_crimes = sorted(crime_counts.items(),
                               key=lambda x: x[1], reverse=True)
        top_crimes = sorted_crimes[:amt]
        top_crimes_by_month[month] = {
            "Top Crimes": [crime for crime, count in top_crimes],
            "Frequencies": [count for crime, count in top_crimes]}
        if display == True:
            if len(monthly_dfs) >= 11:
                print(f"Month {month} most frequent crimes:")
                for crime, freq in top_crimes:
                    print(f"  {crime}: {freq}")
                print("-" * 50)
            # Added function – separates by seasons instead
            elif len(monthly_dfs) == 4:
                print(f"{month} most frequent crimes:")
                for crime, freq in top_crimes:
                    print(f"  {crime}: {freq}")
                print("-" * 50)
        elif display == False:
            pass
    return top_crimes_by_month

def crimes_dct_to_df(crimes_dct):
    ''''Converts the dct from most_frequent_crimes into a pandas df'''
    data = []
    for duration, crime_data in crimes_dct.items():
        for crime, freq in zip(crime_data["Top Crimes"], crime_data["Frequencies"]):
            data.append({"Month/Season": duration, "Crime": crime, "Frequency": freq})
    return pd.DataFrame(data)

# Month Plots
def plot_monthly_crime(monthly_crime_df, aggregate=False):
    '''Plots changes in crime frequencies across months.'''
    if aggregate:
        data_to_plot = monthly_crime_df.groupby("Month/Season")["Frequency"].sum()
        title = "All Intentional Crime by Month"
        ylabel = "Crime Instances"
        legend_title = "Crime"
        data_to_plot.plot(kind="line", marker='o', color='dodgerblue',
                          label="Crime")
        plt.legend(loc="upper right")
    else:
        data_to_plot = monthly_crime_df.groupby([
            "Month/Season", "Crime"])["Frequency"].sum().unstack()
        title = "Monthly Changes in Crime Frequency by Type"
        ylabel = "Crime Frequency (Instances)"
        legend_title = "Crime Type"
        data_to_plot.plot(kind="line", marker='o')
        plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title(title, fontsize=16)
    plt.xlabel("Month", fontsize=9)
    plt.ylabel(ylabel, fontsize=9)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(ticks=range(13))
    plt.ylim(0, data_to_plot.values.max() * 1.2)
    plt.tight_layout() 
    plt.show()
    
def season_separator(df):
    '''Separates dataset into seasons. Returns a dict where keys are season names;
    values are the corresponding smaller datasets'''
    seasons = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8],
               "Fall": [9, 10, 11]}
    season_dfs = {}
    for season, months in seasons.items():
        season_data = df[df['MONTH'].isin(months)]
        season_dfs[season] = season_data.copy()
    return season_dfs

def season_accessor(monthly_dfs, season_input):
    '''Takes in a dictionary of month dataframes and a desired season,
    returns the combined dataframe for that season'''
    seasons = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8],
               "Fall": [9, 10, 11]}
    if isinstance(season_input, str):
        season_months = seasons.get(season_input)
    season_df = monthly_dfs.get(season_months)
    for month in season_months:
        season_df = pd.concat([monthly_dfs[month]])
    print(f"Crime data for {season_input}:")
    return season_df

# Season Plots
def normalize_seasonal_data(df):
    return df.div(df.sum(axis=1), axis=0).copy()

def plot_seasonal_crime(season_crime_df, aggregate=False, title=None):
    '''Optional: Aggregate combines all crimes into one line, default is false.'''
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    if aggregate == True:
        data_to_plot = season_crime_df.groupby('Month/Season')['Frequency'].sum()
        data_to_plot = data_to_plot.reindex(season_order)
        ylabel = 'Crime Instances'
        legend_title = 'Total'
        data_to_plot.plot(kind='line', marker='o', color='royalblue', label='Crime')
        plt.legend(loc='upper right')
    elif aggregate == False:
        data_to_plot = season_crime_df.groupby([
            'Month/Season', 'Crime'])['Frequency'].sum().unstack()
        data_to_plot = data_to_plot.reindex(season_order)
        ylabel = 'Crime Instances'
        legend_title = 'Crime Type'
        data_to_plot.plot(kind='line', marker='o', color='royalblue', label='Crime')
        plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title(title, fontsize=16)
    plt.xlabel('Seasons', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def remove_non_crime(df, exclude_list):
    ''''Remove rows or columns named in the exlcude_lst'''
    to_drop = df[df["Crime"].isin(exclude_list)].index
    return df.drop(index=to_drop)

def filter_crime(df, keep_list):
    '''Keeps rows or columns named in keep_lst'''
    return df[df["Crime"].isin(keep_list)]

def filter_crime_by_str(df, column, keyword):
    '''Keeps rows in a column containing a keyword'''
    filtered_df = df[df[column].str.contains(keyword, case=False, na=False).copy()]
    return filtered_df

def bar_plot_seasonal_crime(season_crime_df):
    '''Plots total crime instances by season in a barplot'''
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    season_totals = season_crime_df.groupby("Month/Season")["Frequency"].sum()
    season_totals = season_totals.reindex(season_order)
    season_totals.plot(kind="bar", color="royalblue", edgecolor="black", figsize=(8, 5))
    plt.title("Total Intentional Crimes by Season", fontsize=16)
    plt.xlabel("Season", fontsize=12)
    plt.ylabel("Total Crime Instances", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

def main():
    crime_df = pd.read_csv(FILENAME)
    crime_df = clean_crime_df(crime_df)
    crime_df = filter_out_2024(crime_df, year=2024)
    print(crime_df)
    # Have the most frequent types of crimes changed over time?
    # Plan: Separate dataset into months, find most frequent crimes per month,
    # then observe change
    all_month_dfs = month_separator(crime_df)
    all_months_top_crimes = most_frequent_crimes(all_month_dfs)
    all_months_top_crimes = most_frequent_crimes(all_month_dfs,
                                                 amt=129, display=False)
    all_months_all_crimes = most_frequent_crimes(all_month_dfs, amt=12)
    all_months_all_crimes_df = crimes_dct_to_df(all_months_all_crimes)
    
    # Visualizing the momthly variation
    # Categorizing (lists for filtering)
    non_intentional_crime_categories = ["SICK ASSIST", "TOWED MOTOR VEHICLE",  
    "SERVICE TO OTHER AGENCY", "FIRE REPORT", "LANDLORD - TENANT", 
    "SICK/INJURED/MEDICAL - PERSON", "M/V ACCIDENT - PROPERTY DAMAGE",
    "M/V ACCIDENT - PERSONAL INJURY", "NOISY PARTY/RADIO-NO ARREST", "PROSTITUTION", 
    "M/V ACCIDENT - OTHER", "PROPERTY - ACCIDENTAL DAMAGE", "PROPERTY - FOUND"]
    all_months_all_intentional_crimes_df = remove_non_crime(
        all_months_all_crimes_df, non_intentional_crime_categories)
    all_months_all_intentional_crimes_df["Frequency"] = pd.to_numeric(
        all_months_all_intentional_crimes_df["Frequency"], errors="coerce")
    bar_plot_seasonal_crime(all_months_all_intentional_crimes_df)
    plot_monthly_crime(all_months_all_intentional_crimes_df, aggregate=True)
    
    # Do seasons affect types of crimes committed?
    # Plan: Same/similar code, just rearrange months into seasons
    all_season_dfs = season_separator(crime_df)
    all_seasons_top_crimes = most_frequent_crimes(all_season_dfs)
    all_seasons_all_crimes = most_frequent_crimes(all_season_dfs, amt=129, display=False)
    all_seasons_all_crimes_df = crimes_dct_to_df(all_seasons_all_crimes)
   
    # Visualizing the seasonal variation
    all_seasons_all_intentional_crimes_df = remove_non_crime(
        all_seasons_all_crimes_df, non_intentional_crime_categories)
    all_seasons_all_intentional_crimes_df["Frequency"] = pd.to_numeric(
        all_seasons_all_intentional_crimes_df["Frequency"], errors="coerce")
    bar_plot_seasonal_crime(all_seasons_all_intentional_crimes_df)
    plot_seasonal_crime(all_seasons_all_intentional_crimes_df,
                        aggregate=True, title='All Intentional Crimes By Season')
   
    # Visualizing specific crimes:
    specific_crime = ['LARCENY', 'ASSAULT', 'INVESTIGATE PERSON', 
    'INVESTIGATE PROPERTY', 'ARSON', 'DRUGS', 'VANDALISM', 'BURGLARY',
    'THREATS', 'MURDER', 'ANIMAL ABUSE', 'ALCOHOL']
    for crime in specific_crime:
        filtered_df = filter_crime_by_str(
            all_seasons_all_intentional_crimes_df, 'Crime', crime)
        plot_seasonal_crime(filtered_df, aggregate=True,
                            title=f'{crime} by Season')
if __name__ == "__main__":
    main()
    