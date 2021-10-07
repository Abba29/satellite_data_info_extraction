import math

"""
    NDVI and its variations
"""


def ndvi(df):
    df["NDVI"] = (df["B4"] - df["B3"]) / (df["B4"] + df["B3"])


def bndvi(df):
    df["BNDVI"] = (df["B4"] - df["B1"]) / (df["B4"] + df["B1"])


def gndvi(df):
    df["GNDVI"] = (df["B4"] - df["B2"]) / (df["B4"] + df["B2"])


def gbndvi(df):
    df["GBNDVI"] = (df["B4"] - (df["B2"] + df["B1"])) / (df["B4"] + (df["B2"] + df["B1"]))


def grndvi(df):
    df["GRNDVI"] = (df["B4"] - (df["B2"] + df["B3"])) / (df["B4"] + (df["B2"] + df["B3"]))


def rbndvi(df):
    df["RBNDVI"] = (df["B4"] - (df["B3"] + df["B1"])) / (df["B4"] + (df["B3"] + df["B1"]))


def pan_ndvi(df):
    df["PAN NDVI"] = (df["B4"] - (df["B3"] + df["B2"] + df["B1"])) / (
                df["B4"] + (df["B3"] + df["B2"] + df["B1"]))


"""
    Indices that fix NDVI's flaws
"""


def arvi(df):
    df["ARVI"] = (((df["B4"] - df["B3"]) / (df["B4"] + df["B3"])) * 1.17) - 0.18


def gari(df):
    df["B-R"] = df["B1"] - df["B3"]
    df["G-(B-R)"] = df["B2"] - df["B-R"]
    df["G+(B-R)"] = df["B2"] + df["B-R"]
    df["num"] = df["B4"] - df["G-(B-R)"]
    df["den"] = df["B4"] - df["G+(B-R)"]
    df["GARI"] = df["num"]/df["den"]
    df.drop(columns=["B-R", "G-(B-R)", "G+(B-R)", "num", "den"], inplace=True)


def evi(df):
    df["EVI"] = ((df["B4"] - df["B3"]) / ((((df["B3"] * 6) - (df["B1"] * 7.5)) + df["B4"]) + 1)) * 2.5


def evi2(df):
    df["EVI2"] = ((df["B4"] - df["B3"]) / ((df["B4"] + df["B3"]) + 1)) * 2.4


def savi(df):
    df["SAVI"] = ((df["B4"] - df["B3"]) / (df["B4"] + df["B3"] + 1)) * (1 + 0.5)


def msavi(df):
    df["a"] = (df["B4"] * 2) + 1
    df["b"] = (df["B4"] - df["B3"]) * 8
    df["power"] = df["a"].apply(lambda x: pow(x, 2))
    df["diff"] = df["power"] - df["b"]
    df["sqrt"] = df["diff"].apply(lambda x: math.sqrt(x))
    df["MSAVI"] = (df["a"] - df["sqrt"]) / 2
    df.drop(columns=["a", "b", "power", "diff", "sqrt"], inplace=True)


def wdrvi(df):
    df["WDRVI"] = ((df["B4"] * 0.1) - df["B3"]) / ((df["B4"] * 0.1) + df["B3"])


def bwdrvi(df):
    df["BWDRVI"] = ((df["B4"] * 0.1) - df["B1"]) / ((df["B4"] * 0.1) + df["B1"])


"""
    Other vegetation indices
"""


def ndgi(df):
    df["NDGI"] = (df["B2"] - df["B3"]) / (df["B2"] + df["B3"])


def norm_g(df):
    df["Norm G"] = (df["B2"]) / (df["B4"] + df["B3"] + df["B2"])


def norm_nir(df):
    df["Norm NIR"] = (df["B4"]) / (df["B4"] + df["B3"] + df["B2"])


def norm_r(df):
    df["Norm R"] = (df["B3"]) / (df["B4"] + df["B3"] + df["B2"])


"""
    Soil indices
"""


def gdvi(df):
    df["GDVI"] = df["B4"] - df["B2"]


def ndsi(df):
    df["NDSI"] = (df["B3"] - df["B4"]) / (df["B3"] + df["B4"])


def ri(df):
    df["R2"] = df["B3"].apply(lambda x: pow(x, 2))
    df["G3"] = df["B2"].apply(lambda x: pow(x, 3))
    df["RI"] = (df["R2"]) / (df["B1"] * df["G3"])
    df.drop(columns=["R2", "G3"], inplace=True)


def io(df):
    df["IO"] = df["B3"] / df["B1"]


def ci(df):
    df["CI"] = (df["B3"] - df["B1"]) / (df["B3"] + df["B1"])


"""
    Utility functions
"""


def calc_ndvis(df):
    ndvi(df)
    bndvi(df)
    gndvi(df)
    gbndvi(df)
    grndvi(df)
    rbndvi(df)
    pan_ndvi(df)


def calc_nvdi_corrections(df):
    arvi(df)
    gari(df)
    evi(df)
    evi2(df)
    savi(df)
    msavi(df)
    wdrvi(df)
    bwdrvi(df)


def calc_other_vegetation_indices(df):
    ndgi(df)
    norm_g(df)
    norm_nir(df)
    norm_r(df)


def calc_soil_indices(df):
    gdvi(df)
    ndsi(df)
    ri(df)
    io(df)
    ci(df)