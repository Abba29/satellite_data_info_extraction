import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from sklearn.preprocessing import MinMaxScaler

from sentinel_building_matrix import sentinel3D
from soil_building_matrix import soil3D

from sentinel_indices import *


"""
    INDICES SELECTION
    (0) NO INDICES CALCULUS
    (1) NDVI, BNDVI, GNDVI, GBNDVI, GRNDVI, RBNDVI, PAN NDVI
    (2) ARVI, GARI, EVI, EVI2, SAVI, MSAVI, WDRVI, BWDRVI
    (3) NDWI, DSWI, NDGI, Norm G, Norm NIR, Norm R
    (4) GDVI, NDSI, MSI, RI, IO, CI
"""
choice1 = 3
choice2 = 1

scaler = MinMaxScaler(feature_range=(0,1))  # normalization

s2_bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8a", "B09", "B11", "B12"]

dates = ["2021-04-20", "2021-04-30", "2021-05-05", "2021-05-10",
         "2021-05-25", "2021-06-04", "2021-06-09", "2021-06-14",
         "2021-07-09", "2021-07-29", "2021-08-03", "2021-08-08",
         "2021-08-18", "2021-08-23", "2021-09-02", "2021-09-07"]

parameters = ["TEMP", "HUM", "PH", "EC", "N", "P", "K"]

soil_dfs = []
sentinel_dfs = []
indices_dfs = []
indices_dfs2 = []

for date in dates:
    
    temp_soil_ndarr = soil3D.sel(date=date)
    temp_soil_df = pd.DataFrame(temp_soil_ndarr.data, columns=parameters)
    
    temp_sentinel_ndarr = sentinel3D.sel(date=date)
    temp_sentinel_df = pd.DataFrame(temp_sentinel_ndarr.data, columns=s2_bands)

    temp_s2_indices_ndarr = sentinel3D.sel(date=date)
    temp_s2_indices_df = pd.DataFrame(temp_s2_indices_ndarr.data, columns=s2_bands)
    
    temp_s2_indices_ndarr2 = sentinel3D.sel(date=date)
    temp_s2_indices_df2 = pd.DataFrame(temp_s2_indices_ndarr2.data, columns=s2_bands)
    
    if choice1 == 0:
        print("No indices calculus")    
    elif choice1 == 1:
        calc_ndvis(temp_s2_indices_df)
    elif choice1 == 2:
        calc_nvdi_corrections(temp_s2_indices_df)
    elif choice1 == 3:
        calc_other_vegetation_indices(temp_s2_indices_df)
    elif choice1 == 4:
        calc_soil_indices(temp_s2_indices_df)
    else:
        print("Incorrect number. \n No index will be calculated. \n Calculating correlation with bands...")
    
    if choice2 == 0:
        print("No indices calculus")    
    elif choice2 == 1:
        calc_ndvis(temp_s2_indices_df2)
    elif choice2 == 2:
        calc_nvdi_corrections(temp_s2_indices_df2)
    elif choice2 == 3:
        calc_other_vegetation_indices(temp_s2_indices_df2)
    elif choice2 == 4:
        calc_soil_indices(temp_s2_indices_df2)
    else:
        print("Incorrect number. \n No index will be calculated. \n Calculating correlation with bands...")
    
    # remove the bands columns
    for band in s2_bands:
        temp_s2_indices_df.drop(columns=band, inplace=True)
        temp_s2_indices_df2.drop(columns=band, inplace=True)
    
    # normalize/standardize soil data
    soil_col_names = temp_soil_df.columns
    temp_soil_df = scaler.fit_transform(temp_soil_df) 
    temp_soil_df = pd.DataFrame(temp_soil_df, columns=soil_col_names)
    
    # normalize/standardize sentinel data
    sentinel_col_names = temp_sentinel_df.columns
    temp_sentinel_df = scaler.fit_transform(temp_sentinel_df)
    temp_sentinel_df = pd.DataFrame(temp_sentinel_df, columns=sentinel_col_names)
    
    # normalize/standardize indices data
    indices_col_names = temp_s2_indices_df.columns
    temp_s2_indices_df = scaler.fit_transform(temp_s2_indices_df)
    temp_s2_indices_df = pd.DataFrame(temp_s2_indices_df, columns=indices_col_names)
    
    # normalize/standardize indices data
    indices_col_names2 = temp_s2_indices_df2.columns
    temp_s2_indices_df2 = scaler.fit_transform(temp_s2_indices_df2)
    temp_s2_indices_df2 = pd.DataFrame(temp_s2_indices_df2, columns=indices_col_names2)
    
    soil_dfs.append(temp_soil_df)
    sentinel_dfs.append(temp_sentinel_df)
    indices_dfs.append(temp_s2_indices_df)
    indices_dfs2.append(temp_s2_indices_df2)

# convert each DataFrame into a Numpy array
soil_df_arrays = [df.to_numpy() for df in soil_dfs]
sentinel_df_arrays = [df.to_numpy() for df in sentinel_dfs]
indices_df_arrays = [df.to_numpy() for df in indices_dfs]
indices_df_arrays2 = [df.to_numpy() for df in indices_dfs2]

# create a 3D matrix from a list of NumPy arrays
soil_norm_matrix = np.array(soil_df_arrays)
sentinel_norm_matrix = np.array(sentinel_df_arrays)
indices_norm_matrix = np.array(indices_df_arrays)
indices_norm_matrix2 = np.array(indices_df_arrays2)


"""
    Create DataArrays (XArray library) for better accessing data
"""
points = np.arange(0, 35, 1)

# create the DataArray using passing coordinates' values and dimensions' names
soil_norm3D = xr.DataArray(soil_norm_matrix, coords=[dates, points, parameters], dims=["date", "point", "parameter"])
sentinel_norm3D = xr.DataArray(sentinel_norm_matrix, coords=[dates, points, s2_bands], dims=["date", "point", "band"])
indices_norm3D = xr.DataArray(indices_norm_matrix, coords=[dates, points, indices_col_names], dims=["date", "point", "index"])
indices_norm3D2 = xr.DataArray(indices_norm_matrix2, coords=[dates, points, indices_col_names2], dims=["date", "point", "index"])

new_dates = [date[-5:] for date in dates]

"""
    Select point, parameter, band and/or index to represent
"""
pnt = 13
par = "EC"
bnd = "B04"
ind = "DSWI"
ind2 = "NDVI"

# tmp1 = soil_norm3D.sel(point=pnt, parameter=par)
# tmp2 = sentinel_norm3D.sel(point=pnt, band=bnd)
tmp3 = indices_norm3D.sel(point=pnt, index=ind)
tmp4 = indices_norm3D2.sel(point=pnt, index=ind2)

# plt.plot(new_dates, tmp1, label=par, linewidth=0.9)
# plt.plot(new_dates, tmp2, label=bnd, linewidth=0.9)
plt.plot(new_dates, tmp3, label=ind, linewidth=0.9)
plt.plot(new_dates, tmp4, label=ind2, linewidth=0.9)

plt.xticks(rotation=45)
plt.legend(loc="upper left")
            
for date in new_dates:
    plt.axvline(x=date,color="darkgray", linewidth=0.2)
            
plt.tight_layout()
plt.savefig("../sentinel_latest.png", dpi=300)  # save plot to .png
plt.close()