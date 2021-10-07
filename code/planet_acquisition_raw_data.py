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

evalscript_bands = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B1","B2","B3","B4"], 
                units: "DN"
            }],
            output: {
                bands: 4,
                sampleType: "INT16"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B1,
                sample.B2,
                sample.B3,
                sample.B4];
    }
"""
#######################################################################################################################
#                                                    PARAMETERS                                                       #
#######################################################################################################################

# desired pixel resolution (bands with lower resolution will be automatically upscaled)
resolution = 3

# longitude and latitude of lower left and upper right corners
strappelli_coords_wgs84 = [13.764835, 42.812177, 13.767109, 42.813841]

strappelli_bbox = BBox(bbox=strappelli_coords_wgs84, crs=CRS.WGS84)
strappelli_size = bbox_to_dimensions(strappelli_bbox, resolution=resolution)

#######################################################################################################################
#                                       DEFINE A DATA COLLECTION FOR PLANET SCOPE                                     #
#######################################################################################################################

collection_id = '<collection-id>'

planet = DataCollection.define_byoc(
    collection_id,
    name='PLANET-SCOPE',
    is_timeless=True
)

#######################################################################################################################
#                                         REQUEST ALL BANDS ON A SPECIFIC DATE                                        #
#######################################################################################################################
request_all_bands = SentinelHubRequest(
    data_folder = "./data",
    evalscript=evalscript_bands,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=planet,
            time_interval=('2021-09-06', '2021-09-08'),
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


