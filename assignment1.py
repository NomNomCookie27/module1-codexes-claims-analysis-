import pandas as pd

# Load the dataset with the correct delimiter '|' and low_memory=False to handle mixed data types
file_path = 'inpatient.csv'
df = pd.read_csv(file_path, delimiter= '|', low_memory=False)