from preprocessing import preprocess_data
from visualization import *
from analysis import *
import pandas as pd
from pandasgui import show


# Load data
df = pd.read_csv(r"C:\Users\liora\Downloads\netflix-report\CONTENT_INTERACTION\ViewingActivity.csv")

# Preprocess data
df = preprocess_data(df)

plot_duration_by_time_unit(df, "hour")
plot_duration_by_title(df, None, 10)
plot_total_duration_by_profile(df)
plot_duration_freq(df)
plot_duration_by_country(df)
plot_duration_by_device(df, 5)


# print()

# print(df['device_type'].unique())
