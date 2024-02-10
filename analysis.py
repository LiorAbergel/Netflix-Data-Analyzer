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

def get_monthly_view_count(df, profile_name=None):
    """Returns a DataFrame with the number of viewing sessions per month."""
    
    filtered_df = df[df['profile_name'] == profile_name] if profile_name else df
    
    filtered_df = filtered_df[['start_time']].copy()
    
    filtered_df['month'] = filtered_df['start_time'].dt.to_period('M')

    filtered_df['month'] = filtered_df['month'].astype(str)
    
    weekly_data = filtered_df.groupby('month').size().reset_index(name='count')

    weekly_data['year'] = weekly_data['month'].str[:4]

    return weekly_data




