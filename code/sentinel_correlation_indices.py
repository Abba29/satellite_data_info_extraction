import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from sentinel_building_matrix import sentinel3D
from soil_building_matrix import soil3D

from sentinel_indices import *


"""
    INDICES SELECTION
    (1) NDVI, BNDVI, GNDVI, GBNDVI, GRNDVI, RBNDVI, PAN NDVI
    (2) ARVI, GARI, EVI, EVI2, SAVI, MSAVI, WDRVI, BWDRVI
    (3) NDWI, DSWI, NDGI, Norm G, Norm NIR, Norm R
    (4) GDVI, NDSI, MSI, RI, IO, CI
"""
choice = 1


scaler = MinMaxScaler(feature_range=(0,1))  # normalization
# scaler = StandardScaler()  # standardization

bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8a", "B09", "B11", "B12"]

dates = ["2021-04-20", "2021-04-30", "2021-05-05", "2021-05-10",
         "2021-05-25", "2021-06-04", "2021-06-09", "2021-06-14",
         "2021-07-09", "2021-07-29", "2021-08-03", "2021-08-08",
         "2021-08-18", "2021-08-23", "2021-09-02", "2021-09-07"]

parameters = ["TEMP", "HUM", "PH", "EC", "N", "P", "K"]

corr_dfs = []

for date in dates:
    
    temp_soil_ndarr = soil3D.sel(date=date)
    temp_df = pd.DataFrame(temp_soil_ndarr.data, columns=parameters)
    
    temp_s2_ndarr = sentinel3D.sel(date=date)

    # adds bands columns after the ones corresponding to parameters
    for i, band in zip(range(0, len(bands)),bands):
        temp_df.insert(len(temp_df.axes[1]), band, pd.Series(temp_s2_ndarr.data[:,i]).astype(int))
    
    if choice == 1:
        calc_ndvis(temp_df)
    elif choice == 2:
        calc_nvdi_corrections(temp_df)
    elif choice == 3:
        calc_other_vegetation_indices(temp_df)
    elif choice == 4:
        calc_soil_indices(temp_df)
    else:
        print("Incorrect number. \n No index will be calculated. \n Calculating correlation with bands...")
    
    print(temp_df)

    # remove the bands columns
    for band in bands:
        temp_df.drop(columns=band, inplace=True)
    
    # there is no need to normalize/standardize, indeed (i.e. we get same results)
    # (for more information, see: https://www.researchgate.net/post/Do_we_need_to_standardize_variables_with_different_scales_before_doing_correlation_analysis)
        
    # # normalize/standardize the data
    # col_names = temp_df.columns
    # temp_df = scaler.fit_transform(temp_df)    
    # temp_df = pd.DataFrame(temp_df, columns=col_names)

    temp_corr = temp_df.corr()
    
    corr_dfs.append(temp_corr)

    # the lower triangle of the correlation matrix will be used as a mask
    lower_triangle = np.tril(temp_corr)

    ax = sns.heatmap(temp_corr, cmap="coolwarm", center=0, vmin=-1, vmax=1, 
                     linewidths=1, square=True, mask=lower_triangle)

    plt.tick_params(axis='both', which='major', labelsize=10, bottom=False,
                    top = False, left = False, labeltop=True, labelbottom=False)
    plt.xticks(rotation=90)
    
    plt.tight_layout()
    plt.savefig("../" + date + "_sentinel_correlation_indices_" + str(choice) + ".png", dpi=300)  # save plot to .png
    plt.close()
    
if choice == 1 or choice == 2 or choice == 3 or choice == 4:
    # save the correlation matrices to .xlsx file [one matrix (i.e. one date) per sheet]
    with pd.ExcelWriter("../sentinel_correlation_indices_" + str(choice) + ".xlsx") as writer:
        for i, date in zip(range(0, len(dates)), dates):
            corr_dfs[i].to_excel(writer, sheet_name=date)
    
    # convert each DataFrame into a Numpy array
    df_arrays = [df.to_numpy() for df in corr_dfs]
    
    # create a 3D matrix from a list of NumPy arrays
    corr_matrix = np.array(df_arrays)
    
    corr_min = np.amin(corr_matrix, axis=0)
    corr_max = np.amax(corr_matrix, axis=0)
    corr_mean = np.mean(corr_matrix, axis=0)
    corr_std = np.std(corr_matrix, axis=0)
    
    # create an array of pd.DataFrames from these values
    col_names = corr_dfs[0].columns
    arr_dfs = [pd.DataFrame(corr_min, columns=col_names),
               pd.DataFrame(corr_max, columns=col_names),
               pd.DataFrame(corr_mean, columns=col_names),
               pd.DataFrame(corr_std, columns=col_names)]
    
    calculated = ["min", "max", "mean", "std"]
    
    # save the min/max/mean/std matrices to .xlsx file [one matrix per sheet]
    with pd.ExcelWriter("../sentinel_correlation_indices_" + str(choice) + "_stats.xlsx") as writer:
        for i, name in zip(range(0, len(calculated)), calculated):
            arr_dfs[i].to_excel(writer, sheet_name=name)



