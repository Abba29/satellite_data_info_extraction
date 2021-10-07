import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from sentinel_building_matrix import sentinel3D

scaler = MinMaxScaler(feature_range=(0,1))  # normalization
# scaler = StandardScaler()  # standardization

bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8a", "B09", "B11", "B12"]


dates = ["2021-04-20", "2021-04-30", "2021-05-05", "2021-05-10",
         "2021-05-25", "2021-06-04", "2021-06-09", "2021-06-14",
         "2021-07-09", "2021-07-29", "2021-08-03", "2021-08-08",
         "2021-08-18", "2021-08-23", "2021-09-02", "2021-09-07"]

sentinel_dfs = []

for date in dates:
    
    temp_sentinel_ndarr = sentinel3D.sel(date=date)
    temp_sentinel_df = pd.DataFrame(temp_sentinel_ndarr.data, columns=bands)
    
    # # normalize/standardize the data
    # sentinel_col_names = temp_sentinel_df.columns
    # temp_sentinel_df = scaler.fit_transform(temp_sentinel_df)
    # temp_sentinel_df = pd.DataFrame(temp_sentinel_df, columns=sentinel_col_names)
    
    sentinel_dfs.append(temp_sentinel_df)
        
# # save the normalized dataframes to .xlsx file [one dataframe (i.e. one date) per sheet]
# with pd.ExcelWriter("../sentinel_normalized_bands.xlsx") as writer:
#     for i, date in zip(range(0, len(dates)), dates):
#         sentinel_dfs[i].to_excel(writer, sheet_name=date)