import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from planet_building_matrix import planet3D

scaler = MinMaxScaler(feature_range=(0,1))  # normalization
# scaler = StandardScaler()  # standardization

bands = ["B1", "B2", "B3", "B4"]

dates = ["2021-04-20", "2021-04-30", "2021-05-05", "2021-05-10",
         "2021-05-25", "2021-06-04", "2021-06-09", "2021-06-14",
         "2021-07-09", "2021-07-29", "2021-08-03", "2021-08-08",
         "2021-08-18", "2021-08-23", "2021-09-02", "2021-09-07"]

planet_dfs = []

for date in dates:
    
    temp_planet_ndarr = planet3D.sel(date=date)
    temp_planet_df = pd.DataFrame(temp_planet_ndarr.data, columns=bands)
    
    # # normalize/standardize the data
    # planet_col_names = temp_planet_df.columns
    # temp_planet_df = scaler.fit_transform(temp_planet_df)
    # temp_planet_df = pd.DataFrame(temp_planet_df, columns=planet_col_names)
    
    planet_dfs.append(temp_planet_df)
        
# # save the normalized dataframes to .xlsx file [one dataframe (i.e. one date) per sheet]
# with pd.ExcelWriter("../planet_normalized_bands.xlsx") as writer:
#     for i, date in zip(range(0, len(dates)), dates):
#         planet_dfs[i].to_excel(writer, sheet_name=date)