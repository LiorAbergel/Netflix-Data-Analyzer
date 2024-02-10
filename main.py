from preprocessing import preprocess_data
from visualization import *
from analysis import *
import pandas as pd
from pandasgui import show


# Load data
df = pd.read_csv(r"C:\Users\liora\Downloads\netflix-report\CONTENT_INTERACTION\ViewingActivity.csv")

# Preprocess data
df = preprocess_data(df)



