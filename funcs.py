import pandas as pd
import numpy as np
import datetime

def calc_percent_missing(no_observations, maxobservations):
    '''This takes the number of missing and maximum observations as inputs. It
    then calculates the no of missing observations as a percentage of the total observations'''
    percent_miss = round((no_observations / maxobservations) * (100 / 1), 2)
    print(f"The percentage of missing values is:\n{percent_miss}")


def calculate_IQR_CV(dataframe):
    '''This function takes a traffic dataframe input, calculates the interquartile range (IQR)
    of the 'CountValue' using numpy and returns it'''
    q3, q1 = np.percentile(dataframe.CountValue, [75, 25])
    IQR = q3 - q1
    return IQR


def show_boundaries(dataframe):
    '''This function takes a traffic dataframe as input, calculates the first and third
    quartile, the interquartile range and the upper and lower boundaries for outliers in
    the dataframe. Additionally, it tests that the lower boundary is not outside the domain
    by dropping to at or below or Zero'''
    Q3, Q1 = np.percentile(dataframe.CountValue, [75, 25])
    IQR_md = Q3 - Q1

    upper_limit_md = Q3 + (IQR_md * 1.5)
    lower_limit_md = Q1 - (IQR_md * 1.5)

    if lower_limit_md < 1:
        lower_limit_md = 1
    else:
        lower_limit_md = Q3 + (IQR_md * 1.5)

    print(f"The first quartile (Q1) is {Q1}")
    print(f"The third quartile (Q3) is {Q3}")
    print(f"The upper boundary for outliers is is {upper_limit_md}")
    print(f"The lower boundary for outliers is is {lower_limit_md}")


def add_day_of_week(dataframe):
    '''This function takes a traffic dataframe as input and creates a day of the week
    column using pandas datetime formating'''
    dataframe['DayOfWeek'] = dataframe['Date'].dt.day_name()
    return dataframe


def convert_to_date_time(dataframe):
    '''This function takes a traffic dataframe as input, it then converts the Date and Time
    columns to datetime format'''
    dataframe['Date'] = pd.to_datetime(dataframe['Date'], infer_datetime_format = True)
    dataframe['Time'] = pd.to_datetime(dataframe['Time'], infer_datetime_format = True)
    return dataframe


def merge_date_time(dataframe):
    '''This function takes a traffic dataframe as input, it merges the 'Date' & 'Time' columns
        and and then sets the date and time as an index. The function then removes the additional Zero
        values created by the datetime function'''
    dataframe['DateTime'] = dataframe["Date"] + ' ' + dataframe["Time"]
    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'], infer_datetime_format=True)
    dataframe.set_index("DateTime", inplace=True)
    dataframe = dataframe.loc[dataframe['CountValue'] != 0]
    return dataframe


def merge_similar_counttypes(dataframe):
    '''This function takes in a traffic dataframe as input, it then maps vehicle categories in the
    'CountType' column to a single merged category and returns the changed dataframe'''
    dataframe['CountType'] = dataframe['CountType'].replace({
        'CAR OCC 1': 'CAR', 'CAR OCC 2': 'CAR', 'CAR OCC 3': 'CAR',
        'CAR OCC 4': 'CAR', 'CAR OCC 5': 'CAR', 'CAR OCC 6': 'CAR',
        'CAR OCC 7': 'CAR', 'CAR OCC 8': 'CAR', 'CAR OCC 9': 'CAR',
        'TAXI OCC 1': 'TAXI', 'TAXI OCC 2': 'TAXI', 'TAXI OCC 3': 'TAXI',
        'TAXI OCC 4': 'TAXI', 'TAXI OCC 5': 'TAXI', 'TAXI OCC 6': 'TAXI',
        'TAXI OCC 7': 'TAXI', 'TAXI OCC 8': 'TAXI', 'TAXI OCC 9': 'TAXI',
        'DBUS': 'BUS', 'OBUS': 'BUS', 'ELDERLY': 'PED', 'CHILD':'PED',
        'TOTAL': 'PEDTOTAL', 'ADULT':'PED', 'HGV 2X': 'HGV', 'HGV 3X': 'HGV',
        'HGV 4X': 'HGV', 'HGV 5+X': 'HGV', 'LGV':'HGV', 'PCU':'OTHER', 'P/C':'OTHER', 'M/C':'OTHER'
    })
    return dataframe


def create_rush_hour(dataframe):
    '''This function maps the hours of the day in the "Hour" feature and creates a new column
    based on whether the hour is considered 'rush hour or not'.'''
    dataframe['Rush_Hour'] = dataframe['Hour'].replace({
        7: 'Rush_Hour', 8: 'Rush_Hour', 9: 'Rush_Hour',
        10: 'Not_Rush_Hour', 11: 'Not_Rush_Hour', 12: 'Not_Rush_Hour',
        13: 'Not_Rush_Hour', 14: 'Not_Rush_Hour', 15: 'Not_Rush_Hour',
        16: 'Rush_Hour', 17: 'Rush_Hour', 18:'Rush_Hour'
    })
    return dataframe


def remove_zeros_cv(dataframe):
    '''This function takes a traffic dataframe as input, checks the 'CountValue'
    column of these datasets for Zero values and drops the entire rows
    if the 'CountValue' contains a Zero'''
    dataframe = dataframe.loc[dataframe['CountValue'] != 0]
    return dataframe

