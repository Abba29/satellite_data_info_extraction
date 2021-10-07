import numpy as np
import pandas as pd

from sklearn.cluster import AgglomerativeClustering

from sentinel_building_matrix import sentinel3D

bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8a", "B09", "B11", "B12"]

dates = ["2021-04-20", "2021-04-30", "2021-05-05", "2021-05-10",
         "2021-05-25", "2021-06-04", "2021-06-09", "2021-06-14",
         "2021-07-09", "2021-07-29", "2021-08-03", "2021-08-08",
         "2021-08-18", "2021-08-23", "2021-09-02", "2021-09-07"]


sentinel_dfs = []

for date in dates:
    
    temp_sentinel_ndarr = sentinel3D.sel(date=date)
    temp_sentinel_df = pd.DataFrame(temp_sentinel_ndarr.data, columns=bands)
    
    sentinel_dfs.append(temp_sentinel_df)


"""
    FOR EACH DAY, FOR EACH BAND, CALCULATE MEAN OF 35 POINT VALUES
"""
mean_dfs = []

for i in range(0, len(sentinel_dfs)):
    temp_df = pd.DataFrame()
    for band in bands:
        temp_df.insert(len(temp_df.axes[1]), band, pd.Series(sentinel_dfs[i][band].mean()))
    mean_dfs.append(temp_df)


"""
    CREATE A LIST OF DATAFRAMES IN WHICH THE ROW WITH MEAN VALUES IS REPEATED 35 TIMES
"""
mean_dfs_repeated = []

for df in mean_dfs:
    temp_df = pd.concat([df]*35, ignore_index=True)
    mean_dfs_repeated.append(temp_df)


"""
    FOR EACH DAY, FOR EACH BAND, CALCULATE THE DIFFERENCE FROM MEAN VALUE FOR 35 POINTS
"""
diff_from_mean_dfs = []

for i in range(0, len(sentinel_dfs)):
    temp_df = pd.DataFrame()
    for band in bands:
        diff = sentinel_dfs[i][band] - mean_dfs_repeated[i][band]
        temp_df.insert(len(temp_df.axes[1]), band, pd.Series(diff))
    diff_from_mean_dfs.append(temp_df)


"""
    FOR EACH POINT, CALCULATE THE MEAN OF THE DIFFERENCE ACROSS ALL THE 16 DAYS
"""
# convert each DataFrame into a Numpy array
df_arrays = [df.to_numpy() for df in diff_from_mean_dfs]

# create a 3D matrix from a list of NumPy arrays
diff_matrix = np.array(df_arrays)

# axis = 0 specifies to calculate the following along the 'dates' axis
diff_mean = np.mean(diff_matrix, axis=0)

diff_mean_df = pd.DataFrame(diff_mean, columns=bands)

diff_mean_df = diff_mean_df.abs()

# # save values to .xlsx file [one matrix per sheet]
# with pd.ExcelWriter("../sentinel_temporal_mean_of_difference_values.xlsx") as writer:
#     diff_mean_df.to_excel(writer)


"""
    CLUSTERING
"""
# empirically found that there is no significant difference from 5 and 6 clusters
clt = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')

# train model
model = clt.fit(diff_mean_df.to_numpy())

# predict clusters
clusters = pd.DataFrame(model.fit_predict(diff_mean_df.to_numpy()))
diff_mean_df["Cluster"] = clusters

# sorted_diff_mean_df = diff_mean_df.sort_values(by='Cluster')

cl0 = diff_mean_df[diff_mean_df["Cluster"] == 0]
cl1 = diff_mean_df[diff_mean_df["Cluster"] == 1]
cl2 = diff_mean_df[diff_mean_df["Cluster"] == 2]
cl3 = diff_mean_df[diff_mean_df["Cluster"] == 3]
cl4 = diff_mean_df[diff_mean_df["Cluster"] == 4]


##############################################################################
#                                                                            #
#            SAMPLE POINTS REDUCTIONS (BASED ON DETECTED CLUSTERS)           #
#                                                                            #
##############################################################################

# list of pd.DataFrame (clusters)
cluster_dfs = [cl0, cl1, cl2, cl3, cl4]

# drop cluster label (not needed for successive calculation)
for df in cluster_dfs:
    df.drop(labels="Cluster", axis=1, inplace=True)

cl_mean_dfs = []

# for each cluster, calculate cluster's mean point
for i in range(0, len(cluster_dfs)):
    temp_df = pd.DataFrame()
    for band in bands:
        temp_df.insert(len(temp_df.axes[1]), band, pd.Series(cluster_dfs[i][band].mean()))
    cl_mean_dfs.append(temp_df)
    

cl_mean_dfs_repeated = []

# for each cluster, repeat mean point's values as many times as cluster's dimension
# (needed to calculate difference of each cluster's point from cluster's mean point)
for i in range(0, len(cluster_dfs)):
    temp_df = pd.concat([cl_mean_dfs[i]]*len(cluster_dfs[i]), ignore_index=True)
    cl_mean_dfs_repeated.append(temp_df)

# to make dataframes row indices match (difference will look also at the same index)
for i in range(0, len(cluster_dfs)):
    cl_mean_dfs_repeated[i].index = cluster_dfs[i].index

cl_diff_from_mean_dfs = []

# for each cluster, calculate the difference of each point from cluster's mean point
for i in range(0, len(cluster_dfs)):
    temp_df = pd.DataFrame()
    for band in bands:
        diff = cluster_dfs[i][band] - cl_mean_dfs_repeated[i][band]
        temp_df.insert(len(temp_df.axes[1]), band, pd.Series(diff))
    cl_diff_from_mean_dfs.append(temp_df.abs())

# add "Sum" column (sum of differences) and "Matches" (used next)
for df in cl_diff_from_mean_dfs:
    df["Sum"] = df.sum(axis=1)
    df["Matches"] = pd.Series(np.zeros(len(df)), index=df.index)


"""
    FIND NEAREST POINT TO THE CLUSTER'S MEAN POINT
"""
# for each band, add 1 to "Matches" if that point has the minimum difference from mean point 
for df in cl_diff_from_mean_dfs:
    temp_df = df.min()
    for band in bands:
        indices_lst = df.index[df[band] == temp_df[band]].tolist()
        for index in indices_lst:
            df.at[index, 'Matches'] += 1
