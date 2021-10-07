from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, DataCollection, bbox_to_dimensions

#######################################################################################################################
#                                                 CONFIGURATION                                                       #
#######################################################################################################################
from sentinelhub import SHConfig

config = SHConfig()

config.instance_id = '<your-instance-id>'
config.sh_client_id = '<your-client-id>'
config.sh_client_secret = '<your-client-secret>'

config.save()

#######################################################################################################################
#                                                  EVALSCRIPT                                                         #
#######################################################################################################################

# Sentinel2-L2A missing band B10 (included in Sentinel2-L1C instead)

evalscript_all_bands = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09", "B11","B12"], 
                units: "DN"
            }],
            output: {
                bands: 12,
                sampleType: "INT16"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B01,
                sample.B02,
                sample.B03,
                sample.B04,
                sample.B05,
                sample.B06,
                sample.B07,
                sample.B08,
                sample.B8A,
                sample.B09,
                sample.B11,
                sample.B12];
    }
"""
#######################################################################################################################
#                                                    PARAMETERS                                                       #
#######################################################################################################################

# desired pixel resolution (bands with lower resolution will be automatically upscaled)
resolution = 10

# longitude and latitude of lower left and upper right corners
strappelli_coords_wgs84 = [13.764835, 42.812177, 13.767109, 42.813841]

strappelli_bbox = BBox(bbox=strappelli_coords_wgs84, crs=CRS.WGS84)
strappelli_size = bbox_to_dimensions(strappelli_bbox, resolution=resolution)

#######################################################################################################################
#                                         REQUEST ALL BANDS ON A SPECIFIC DATE                                        #
#######################################################################################################################
request_all_bands = SentinelHubRequest(
    data_folder = "./data",
    evalscript=evalscript_all_bands,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=('2021-09-05', '2021-09-06'),
            mosaicking_order='mostRecent'
    )],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF)
    ],
    bbox=strappelli_bbox,
    size=strappelli_size,
    config=config
)

all_bands_response = request_all_bands.get_data(save_data=True)


