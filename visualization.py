import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from cycler import cycler
from analysis import *
import numpy as np
import seaborn as sns

VALID_TIME_UNITS = ['hour', 'weekday']

def validate_profile_name(df, profile_name):
    valid_profile_names = df["profile_name"].unique()
    if profile_name and profile_name not in valid_profile_names:
        raise ValueError(f'Invalid profile name. Please choose from: {", ".join(valid_profile_names)}')

def validate_time_unit(time_unit):
    if time_unit and time_unit not in VALID_TIME_UNITS:
        raise ValueError(f'Invalid time unit. Please choose from: {", ".join(VALID_TIME_UNITS)}')

def validate_top_n(top_n):
    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError(f"top_n must be an integer greater than 0.")

def validate_inputs(df, time_unit=None, profile_name=None, top_n=10):
    try:
        validate_profile_name(df, profile_name)
        validate_time_unit(time_unit)
        validate_top_n(top_n)
    except ValueError as e:
        print(f'Error: {e}')
        return False
    return True

def format_profile_name(profile_name=None):
    """Formats the profile name for use in plot titles."""
    profile_name = profile_name or 'All Profiles'
    return f'- {profile_name}'
    
def set_custom_plot_style(figsize=(10, 5)):
    """Sets a custom plot style with a black background and red bars."""
    colors = cycler('color', ['#FF0000'])  # Red color for bars
    plt.rc('axes', facecolor='black', edgecolor='white', axisbelow=True, grid=True, prop_cycle=colors)
    plt.rc('grid', color='w', linestyle='solid')
    plt.rc('xtick', direction='out', color='gray')
    plt.rc('ytick', direction='out', color='gray')
    plt.rc('patch', edgecolor='#E6E6E6') # Gray color for bar edges
    plt.rc('lines', linewidth=2)
    plt.figure(figsize=figsize)

def plot_bar_chart(x, y, xlabel, ylabel, title, rotation=None, annotate=False):
    """Plots a bar chart with the given parameters."""
    set_custom_plot_style()

    plt.bar(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if rotation:
        plt.xticks(rotation=rotation)

    if annotate:
        for i, value in enumerate(y):
            plt.text(i, value + 0.1, f'{value:.2f}', ha='center', va='bottom', color='white')

    if xlabel == 'Country':
        # Set the scale of the y-axis to logarithmic
        plt.yscale('log')
    
    elif xlabel == 'Hour':
        # Set the x-axis to show all hours of the day
        plt.xticks(range(24))

    plt.show()

def plot_bar_duration_by_time_unit(df, time_unit, profile_name=None):
    """Plots a bar chart of the total duration watched per time unit (weekday/hour)"""

    if not validate_inputs(df, time_unit, profile_name):
        return
    
    result_df = get_duration_by(df, time_unit, profile_name)

    title = f'Total Duration by {time_unit.capitalize()} {format_profile_name(profile_name)}'

    plot_bar_chart(result_df[time_unit], result_df['duration'],
                   time_unit.capitalize(), f'Total Duration ({time_unit.capitalize()}s)',
                   title, rotation=0, annotate=False)
    
def plot_bar_duration_by_title(df, profile_name=None, top_n=10):
    """Plots a bar chart of the total duration watched per title"""

    if not validate_inputs(df, None, profile_name, top_n):
        return

    result_df = get_duration_by_title(df, profile_name)[:top_n]

    # Use the bidi algorithm to handle Hebrew text
    titles_hebrew = [get_display(title) for title in result_df['title_name']]

    title = f'Total Duration by Title {format_profile_name(profile_name)}'
    plot_bar_chart(titles_hebrew, result_df['duration'],
                   'Title', 'Total Duration (Hours)', title,
                   rotation=45, annotate=False)

def plot_bar_total_duration_by_profile(df):
    """Plots a bar chart of the total duration watched per profile."""
    
    result_df = get_total_duration_by_profile(df)

    # Calculate the total duration for all profiles
    total_duration_all_profiles = result_df['duration'].sum()

    # Plot total duration for each profile
    plot_bar_chart(result_df['profile_name'], result_df['duration'],
                   'Profile Name', 'Total Duration (Hours)',
                   'Total Duration for Each Profile \n' +
                   f'(Total Duration for All Profiles: {total_duration_all_profiles:.2f} Hours)',
                   rotation=0, annotate=True)

def plot_bar_duration_freq(df, profile_name=None):
    """Plots a chart of the total duration watched per duration category (short/medium/long)"""

    if not validate_inputs(df, None, profile_name):
        return
        
    result_df = get_duration_freq(df, profile_name)
    
    title = f'Duration Frequency {format_profile_name(profile_name)}'
    plot_bar_chart(result_df['duration_cat'], result_df['duration'],
                   'Duration Category', 'Total Duration (Hours)', title,
                   annotate=False)

def plot_bar_duration_by_country(df, top_n=10, profile_name=None):
    """Plots a bar chart of the total duration watched per country"""

    if not validate_inputs(df, None, profile_name, top_n):
        return
    
    result_df = get_duration_by_country(df, profile_name)[:top_n]

    title = f'Total Duration by Country {format_profile_name(profile_name)}'
    plot_bar_chart(result_df['country'], result_df['duration'],
                   'Country', 'Total Duration (Hours)', title,
                   rotation=0, annotate=True)
    
def plot_bar_duration_by_device(df, top_n=5, profile_name=None):
    """Plots a bar chart of the total duration watched per device"""

    if not validate_inputs(df, None, profile_name, top_n):
        return
    
    result_df = get_duration_by_device(df, profile_name)[:top_n]

    title = f'Total Duration by Device {format_profile_name(profile_name)}'
    plot_bar_chart(result_df['device_type'], result_df['duration'],
                   'Device Type', 'Total Duration (Hours)', title,
                   rotation=90, annotate=False)

def plot_graph_viewing_frequency(df, profile_name=None):

    if not validate_inputs(df, None, profile_name):
        return  

    # Group data by 'month' and count the number of viewing sessions
    monthly_data = get_monthly_view_count(df, profile_name)

    # Filter to keep only January data
    january_data = monthly_data[monthly_data['month'].str.endswith('-01')]

    # Extract year from 'month' column to use as labels
    january_years = january_data['month'].str[:4]

    # Plot the monthly viewing frequency
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data['month'], monthly_data['count'], linestyle='-', color='skyblue')
    plt.title('Viewing Frequency')
    plt.xlabel('Year')
    plt.ylabel('Number of Viewing Sessions')

    # Set x-axis tick positions and labels for January
    plt.xticks(january_data['month'], january_years, rotation=45)

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_heatmap_viewing_frequency(df, profile_name=None):

    if not validate_inputs(df, None, profile_name):
        return  

    # Group data by 'month' and count the number of viewing sessions
    monthly_data = get_monthly_view_count(df, profile_name)

    # Extract year and month components
    monthly_data['year'] = monthly_data['month'].str[:4]
    monthly_data['month'] = monthly_data['month'].str[-2:].astype(int)

    # Pivot the data to create a matrix of viewing frequency by month and year
    heatmap_data = monthly_data.pivot(index='year', columns='month', values='count')

    # Plot the heatmap using Seaborn
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='.0f', linewidths=0.5)
    plt.title('Viewing Frequency by Month')
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.tight_layout()
    plt.show()




    
        
    

        
    
        
     

    
