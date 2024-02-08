import pandas as pd
from preprocessing import custom_weekday_order

def get_duration_by(df, by, profile_name=None):
    """Returns a dataframe with the total duration watched per 'by' parameter"""

    filtered_df = df[df['profile_name'] == profile_name] if profile_name else df

    filtered_df = filtered_df.groupby(by)['duration'].sum().sort_index().reset_index()

    filtered_df['duration'] = filtered_df['duration'].dt.total_seconds() / 3600

    return filtered_df

def get_duration_by_title(df, profile_name=None):
    """Returns a dataframe with the total duration watched per title"""
    return get_duration_by(df, 'title_name', profile_name)

def get_total_duration_by_profile(df):
    """Returns a dataframe with the total duration watched per profile"""
    return get_duration_by(df, 'profile_name')

def get_duration_freq(df, profile_name=None):
    """Returns a dataframe with the total duration watched per length (short/medium/long)"""
    return get_duration_by(df, 'duration_cat', profile_name)

def get_duration_by_country(df, profile_name=None):
    """Returns a dataframe with the total duration watched per country"""
    return get_duration_by(df, 'country', profile_name)

def get_duration_by_device(df, profile_name=None):
    """Returns a dataframe with the total duration watched per device"""
    return get_duration_by(df, 'device_type', profile_name)

def get_sessions(df, profile_name=None):
    """Returns a dataframe that contains only the watching sessions found in the data
    session = entry with start time in proximity of 10 minutes from the previous entry's end time
    (Data is sorted by start time)"""




