import pandas as pd

SHORT_DURATION = 30
MEDIUM_DURATION = 60

# Define the order of the weekdays in Israel
custom_weekday_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def drop_empty_supplemental_video_type(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows where 'Supplemental Video Type' column is empty , which means it's a watching session and not watching a trailer/recap"""
    df = df[df['Supplemental Video Type'].isna()]
    return df

def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drops unnecessary columns from the DataFrame."""
    return df.drop(['Attributes', 'Supplemental Video Type', 'Bookmark', 'Latest Bookmark'], axis=1)

def change_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Change column names to be more readable."""
    return df.rename(columns={'Profile Name': 'profile_name', 'Start Time': 'start_time', 'Duration': 'duration', 'Title': 'title', 'Device Type': 'device_type', 'Country': 'country'})

def convert_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert 'Start Time' column to datetime and 'Duration' column to timedelta"""
    df['start_time'] = pd.to_datetime(df['start_time'], utc=True).dt.tz_convert('Israel')
    df['duration'] = pd.to_timedelta(df['duration'])
    return df

def filter_duration(df: pd.DataFrame) -> pd.DataFrame:
    """Filter dataframe to not contain duration under 1 minute"""
    return df.loc[(df['duration'] > '0 days 00:01:00')]

def add_end_time(df: pd.DataFrame) -> pd.DataFrame:
    """Add end time column to dataframe"""
    df['end_time'] = df['start_time'] + df['duration']
    return df

def categorize_duration(duration: pd.Timedelta) -> str:
    """Categorize the duration of a show/movie into 3 categories."""
    total_minutes = duration.total_seconds() / 60

    if total_minutes < SHORT_DURATION:
        return f"less than {SHORT_DURATION} mins"
    elif total_minutes <= MEDIUM_DURATION:
        return f"{SHORT_DURATION + 1}–{MEDIUM_DURATION} mins"
    else:
        return f"more than {MEDIUM_DURATION} mins"

def extract_title(s: str) -> str:
    """Get the title of the show/movie from the 'title' column"""
    # Hebrew title
    if '\u200e' in s or '\u200f' in s:
        return s.replace("\u200e\u200f", ":").split(":")[-1].strip()
    else:
        # English title
        return s.split(':')[0].strip()

def add_weekday_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add weekday column to dataframe"""
    df['weekday'] = df['start_time'].dt.day_name()
    return df

def convert_weekday_column(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the 'weekday' column to a categorical type with the order accepted in Israel"""
    df['weekday'] = pd.Categorical(df['weekday'], categories=custom_weekday_order, ordered=True)
    return df

def add_hour_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add hour column to dataframe"""
    df['hour'] = df['start_time'].dt.hour
    return df

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Reorder columns in the dataframe"""
    return df[['profile_name', 'start_time', 'duration', 'end_time', 'duration_cat', 'weekday', 'hour', 'title_name', 'title', 'device_type', 'country']]

def preprocess_data(df : pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data for the analysis"""

    df = drop_empty_supplemental_video_type(df)
    df = drop_unnecessary_columns(df)
    df = change_column_names(df)
    df = convert_datetime_columns(df)
    df = filter_duration(df)
    df = add_end_time(df)
    df['duration_cat'] = df['duration'].apply(categorize_duration)
    df['title_name'] = list(map(extract_title, df['title']))
    df = add_weekday_column(df)
    df = convert_weekday_column(df)
    df = add_hour_column(df)
    df = reorder_columns(df)

    return df





