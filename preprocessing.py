import pandas as pd
import matplotlib.pyplot as plt
from bidi.algorithm import get_display  # bidi library for Hebrew text support
import re

SHORT_DURATION = 30
MEDIUM_DURATION = 60

# Define the order of the weekdays in Israel
custom_weekday_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def preprocess_data(df):
    """Preprocess the data for the analysis"""

    # Drop rows where 'Supplemental Video Type' column is empty , which means it's a watching session and not watching a trailer/recap
    df = df[df['Supplemental Video Type'].isna()]

    # Drop unnecessary columns
    df = df.drop(['Attributes', 'Supplemental Video Type', 'Bookmark', 'Latest Bookmark'], axis=1)

    # Change column names to be more readable
    df.columns = ['profile_name', 'start_time', 'duration', 'title', 'device_type', 'country']

    # Convert 'Start Time' column to datetime
    df['start_time'] = pd.to_datetime(df['start_time'], utc=True).dt.tz_convert('Israel')

    # Convert Duration column to datetime
    df['duration'] = pd.to_timedelta(df['duration'])

    # Filter dataframe to not contain duration under 1 minute
    df = df.loc[(df['duration'] > '0 days 00:01:00')]

    # Add end time column to dataframe
    df['end_time'] = df['start_time'] + df['duration']

    def categorize_duration(duration):
        """Categorize the duration of a show/movie into 3 categories: less than 30 mins, 31–60 mins, more than 1 hour"""

        total_minutes = duration.total_seconds() / 60

        if total_minutes < 30:
            return f"less than {SHORT_DURATION} mins"
        
        elif 30 <= total_minutes < 60:
            return f"{SHORT_DURATION + 1}–{MEDIUM_DURATION} mins"
        
        else:
            return f"more than {MEDIUM_DURATION} mins"

    # Categorize duration length
    df['duration_cat'] = df['duration'].apply(categorize_duration)

    def get_title(s):
        """Get the title of the show/movie from the 'title' column"""
        # Hebrew title
        if '\u200e' in s or '\u200f' in s:
            return s.replace("\u200e\u200f", ":").split(":")[-1].strip()
        else:
            # English title
            return s.split(':')[0].strip()
        
    df['title_name'] = list(map(get_title, df['title']))

    # Add weekday column to dataframe
    df['weekday'] = df['start_time'].dt.day_name()

    # Convert the 'weekday' column to a categorical type with the order accepted in Israel
    df['weekday'] = pd.Categorical(df['weekday'], categories=custom_weekday_order, ordered=True)

    # Add hour column to dataframe
    df['hour'] = df['start_time'].dt.hour

    def categorize_device(device):
        """Categorize the device type into 3 categories: TV, Computer, Mobile/Tablet"""

        if re.search(r'TV', device):
            return 'TV'
        
        elif re.search(r'Computer|PC', device):
            return 'Computer'
        
        elif re.search(r'Iphone', device):
            return 'Mobile'
        
        else:
            return None

    df['device_cat'] = None

    # Reorder columns in dataframe
    df = df[['profile_name', 'start_time', 'duration', 'end_time', 'duration_cat', 'weekday', 'hour', 'title_name', 'title', 'device_type', 'country']]

    return df





