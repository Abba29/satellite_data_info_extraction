import os
import glob
import numpy as np
import pandas as pd
import xarray as xr

def clean_soil_dataframe(df):
    
    df.drop(columns = [0, 1, 2, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 21, 22, 24, 25, 26, 27], inplace=True)
    df.rename(columns = {5: "TEMP", 8: "HUM", 11: "PH", 14: "EC", 17: "N", 20: "P", 23: "K"}, inplace=True)

"""
    Create a 3D matrix for soil parameters
"""

# get all the .csv files in the specified directory
csvfiles = glob.glob(os.path.join("../raw_data/soil", '*.csv'))

# a list to hold multiple Pandas DataFrames
dataframes = []

# loop through the files and read them with Pandas
for file in csvfiles:
    df = pd.read_csv(file, sep = ",", header = None, encoding = "cp1252")
    clean_soil_dataframe(df)
    dataframes.append(df)

# convert each DataFrame into a Numpy array
df_arrays = [df.to_numpy() for df in dataframes]

# create a 3D matrix from a list of NumPy arrays
soil_matrix = np.array(df_arrays)


"""
    Create a DataArray (XArray library) for better accessing data
"""

# define coordinates' values (i.e. the ticks of different axes)
dates = ["2021-04-20", "2021-04-30", "2021-05-05", "2021-05-10",
         "2021-05-25", "2021-06-04", "2021-06-09", "2021-06-14",
         "2021-07-09", "2021-07-29", "2021-08-03", "2021-08-08",
         "2021-08-18", "2021-08-23", "2021-09-02", "2021-09-07"]
parameters = ["TEMP", "HUM", "PH", "EC", "N", "P", "K"]
points = np.arange(0, 35, 1)

# create the DataArray using passing coordinates' values and dimensions' names
soil3D = xr.DataArray(soil_matrix, coords=[dates, points, parameters], dims=["date", "point", "parameter"])

# example of data selection
arr = soil3D.sel(date="2021-04-20", parameter="N")

# # save the 3D matrix to .xlsx file [one dataframe (i.e. one date) per sheet]
# with pd.ExcelWriter("../processed_data/soil_matrix.xlsx") as writer:
#     for i, date in zip(range(0, len(dates)), dates):
#         dataframes[i].to_excel(writer, sheet_name=date)
