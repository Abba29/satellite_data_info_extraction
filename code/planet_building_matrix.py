import os
import glob
import numpy as np
import pandas as pd
import xarray as xr

from osgeo import gdal

# stop GDAL printing both warnings and errors to STDERR
gdal.PushErrorHandler('CPLQuietErrorHandler')

# make GDAL raise python exceptions for errors (warnings won't raise an exception)
gdal.UseExceptions()


def calculate_satellite_coords(dataset):
    
    (upper_left_x, res_x, rotation_x, upper_left_y, rotation_y, res_y) = ds.GetGeoTransform()
    
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    
    # coordinates of the center of the pixel in the upper left corner 
    xstart = upper_left_x + res_x/2
    ystart = upper_left_y + res_y/2

    # all possible coordinates values
    x = np.arange(xstart, xstart + xsize*res_x, res_x)
    y = np.arange(ystart, ystart + ysize*res_y, res_y)
    
    # due to float operation errors, we have 64 elements instead of 63 for 'x'
    x = x[:-1]  # remove the last element of 'x' (the one 'out of bounds')

    x = np.tile(x, ysize)  # repeat the array 'x' for 'ysize' times
    y = np.repeat(y, xsize)  # repeat elements of 'y' for 'xsize' times (each element
    
    return x, y


def calculate_corresponding_coords(sample_points_coords, sat_longs, sat_lats):
    
    nearest_longs, nearest_lats = [0, 0]
    
    for lon, lat in zip(sample_points_coords["longitude"], sample_points_coords["latitude"]):
        nearest_lon = min(sat_longs, key= lambda longitude: abs(longitude - lon))
        nearest_lat = min(sat_lats, key= lambda latitude: abs(latitude - lat))
        
        nearest_longs = np.append(nearest_longs, nearest_lon)
        nearest_lats = np.append(nearest_lats, nearest_lat)
    
    # remove the first element (i.e. '0')
    nearest_longs = nearest_longs[1:]
    nearest_lats = nearest_lats[1:]
    
    return nearest_longs, nearest_lats
    
    

"""
    Create a 3D matrix for satellite bands
"""

# read .csv file containing sample points' coordinates into a Pandas DataFrame
coordinates = pd.read_csv("../res/sample_points.csv")
coordinates.drop(columns=["point"], inplace=True)

# get all the .tiff files in the specified directory
tiff_files = glob.glob(os.path.join("../raw_data/planet", '*.tiff'))  # DIFF

# a list to hold multiple Pandas DataFrames
dataframes = []

# parameters to store coordinates of satellite data and the ones corresponding to sample points
x, y, nearest_longitudes, nearest_latitudes = [np.empty(0), np.empty(0), np.empty(0), np.empty(0)]

# loop through the files and read them with Pandas
for file in tiff_files:
    ds = gdal.Open(file)
    
    # all .tiff files have same dimensions, so coords of satellite data is calculated once
    if (len(x) == 0) & (len(y) == 0):
        x, y = calculate_satellite_coords(ds)
    
    bands = [ds.GetRasterBand(i) for i in range(1,5)]  # DIFF
    ar = [bands[i].ReadAsArray() for i in range(len(bands))]
    flat = [ar[i].flatten() for i in range(len(ar))]

    ds = None  # close the dataset
    
    df = pd.DataFrame({"Longitude":x, "Latitude":y, "B1":flat[0],
                       "B2":flat[1], "B3":flat[2], "B4":flat[3]})  # DIFF
    
    # since coords of satellite data remain the same, these can be calculated once
    if (len(nearest_longitudes) == 0) & (len(nearest_latitudes) == 0):
        nearest_longitudes, nearest_latitudes = calculate_corresponding_coords(coordinates, x, y)
    
    new_df = pd.DataFrame()
    
    for nlon, nlat in zip(nearest_longitudes, nearest_latitudes):
        new_row = df.loc[(df["Longitude"] == nlon) & (df["Latitude"] == nlat)]
        new_df = new_df.append(new_row, ignore_index=True)
    
    new_df.drop(columns=["Longitude", "Latitude"], inplace=True)
    
    dataframes.append(new_df)


# convert each DataFrame into a Numpy array
df_arrays = [df.to_numpy() for df in dataframes]

# create a 3D matrix from a list of NumPy arrays
planet_matrix = np.array(df_arrays)

"""
    Create a DataArray (XArray library) for better accessing data
"""

# define coordinates' values (i.e. the ticks of different axes)
dates = ["2021-04-20", "2021-04-30", "2021-05-05", "2021-05-10",
         "2021-05-25", "2021-06-04", "2021-06-09", "2021-06-14",
         "2021-07-09", "2021-07-29", "2021-08-03", "2021-08-08",
         "2021-08-18", "2021-08-23", "2021-09-02", "2021-09-07"]
bands = ["B1", "B2", "B3", "B4"]
points = np.arange(0, 35, 1)

# create the DataArray using passing coordinates' values and dimensions' names
planet3D = xr.DataArray(planet_matrix, coords=[dates, points, bands], dims=["date", "point", "band"])

# example of data selection
arr = planet3D.sel(date="2021-04-20", band=["B1", "B2"])

# # save the 3D matrix to .xlsx file [one dataframe (i.e. one date) per sheet]
# with pd.ExcelWriter("../processed_data/planet_matrix.xlsx") as writer:    
#     for i, date in zip(range(0, len(dates)), dates):
#         dataframes[i].to_excel(writer, sheet_name=date)
