import math

"""
    NDVI and its variations
"""


def ndvi(df):
    df["NDVI"] = (df["B08"] - df["B04"]) / (df["B08"] + df["B04"])


def bndvi(df):
    df["BNDVI"] = (df["B08"] - df["B02"]) / (df["B08"] + df["B02"])


def gndvi(df):
    df["GNDVI"] = (df["B08"] - df["B03"]) / (df["B08"] + df["B03"])


def gbndvi(df):
    df["GBNDVI"] = (df["B08"] - (df["B03"] + df["B02"])) / (df["B08"] + (df["B03"] + df["B02"]))


def grndvi(df):
    df["GRNDVI"] = (df["B08"] - (df["B03"] + df["B04"])) / (df["B08"] + (df["B03"] + df["B04"]))


def rbndvi(df):
    df["RBNDVI"] = (df["B08"] - (df["B04"] + df["B02"])) / (df["B08"] + (df["B04"] + df["B02"]))


def pan_ndvi(df):
    df["PAN NDVI"] = (df["B08"] - (df["B04"] + df["B03"] + df["B02"])) / (
                df["B08"] + (df["B04"] + df["B03"] + df["B02"]))


"""
    Indices that fix NDVI's flaws
"""


def arvi(df):
    df["ARVI"] = (((df["B08"] - df["B04"]) / (df["B08"] + df["B04"])) * 1.17) - 0.18


def gari(df):
    df["B-R"] = df["B02"] - df["B04"]
    df["G-(B-R)"] = df["B03"] - df["B-R"]
    df["G+(B-R)"] = df["B03"] + df["B-R"]
    df["num"] = df["B08"] - df["G-(B-R)"]
    df["den"] = df["B08"] - df["G+(B-R)"]
    df["GARI"] = df["num"]/df["den"]
    df.drop(columns=["B-R", "G-(B-R)", "G+(B-R)", "num", "den"], inplace=True)


def evi(df):
    df["EVI"] = ((df["B08"] - df["B04"]) / ((((df["B04"] * 6) - (df["B02"] * 7.5)) + df["B08"]) + 1)) * 2.5


def evi2(df):
    df["EVI2"] = ((df["B08"] - df["B04"]) / ((df["B08"] + df["B04"]) + 1)) * 2.4


def savi(df):
    df["SAVI"] = ((df["B08"] - df["B04"]) / (df["B08"] + df["B04"] + 1)) * (1 + 0.5)


def msavi(df):
    df["a"] = (df["B08"] * 2) + 1
    df["b"] = (df["B08"] - df["B04"]) * 8
    df["power"] = df["a"].apply(lambda x: pow(x, 2))
    df["diff"] = df["power"] - df["b"]
    df["sqrt"] = df["diff"].apply(lambda x: math.sqrt(x))
    df["MSAVI"] = (df["a"] - df["sqrt"]) / 2
    df.drop(columns=["a", "b", "power", "diff", "sqrt"], inplace=True)


def wdrvi(df):
    df["WDRVI"] = ((df["B08"] * 0.1) - df["B04"]) / ((df["B08"] * 0.1) + df["B04"])


def bwdrvi(df):
    df["BWDRVI"] = ((df["B08"] * 0.1) - df["B02"]) / ((df["B08"] * 0.1) + df["B02"])


"""
    Other vegetation indices
"""


def ndwi(df):
    df["NDWI"] = (df["B08"] - df["B11"]) / (df["B08"] + df["B11"])


def dswi(df):
    df["DSWI"] = (df["B08"] + df["B03"]) / (df["B11"] + df["B04"])


def ndgi(df):
    df["NDGI"] = (df["B03"] - df["B04"]) / (df["B03"] + df["B04"])


def norm_g(df):
    df["Norm G"] = (df["B03"]) / (df["B08"] + df["B04"] + df["B03"])


def norm_nir(df):
    df["Norm NIR"] = (df["B08"]) / (df["B08"] + df["B04"] + df["B03"])


def norm_r(df):
    df["Norm R"] = (df["B04"]) / (df["B08"] + df["B04"] + df["B03"])


"""
    Soil indices
"""


def gdvi(df):
    df["GDVI"] = df["B08"] - df["B03"]


def ndsi(df):
    df["NDSI"] = (df["B04"] - df["B08"]) / (df["B04"] + df["B08"])


def msi(df):
    df["MSI"] = df["B11"] / df["B08"]


def ri(df):
    df["R2"] = df["B04"].apply(lambda x: pow(x, 2))
    df["G3"] = df["B03"].apply(lambda x: pow(x, 3))
    df["RI"] = (df["R2"]) / (df["B02"] * df["G3"])
    df.drop(columns=["R2", "G3"], inplace=True)


def io(df):
    df["IO"] = df["B04"] / df["B02"]


def ci(df):
    df["CI"] = (df["B04"] - df["B02"]) / (df["B04"] + df["B02"])


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
    ndwi(df)
    dswi(df)
    ndgi(df)
    norm_g(df)
    norm_nir(df)
    norm_r(df)


def calc_soil_indices(df):
    gdvi(df)
    ndsi(df)
    msi(df)
    ri(df)
    io(df)
    ci(df)