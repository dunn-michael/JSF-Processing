import rasterio
import rasterio.features
import rasterio.warp
from rasterio.plot import show

UAV_image = rasterio.open('20240416-201317-UTC_0-2024-04-16_oahu_kohola_HFB5m_kuleana_spot_1-IVER3-3099_WP4-L.Tiff', 'r')
print("---=UAV IMAGE=---")
print(UAV_image)
print("---=UAV IMAGE=---")
# new_tif = rasterio.open('new.Tiff','w',
#                         driver='GTiff',
#                         height = UAV_image.height,
#                         width = UAV_image.width, 
#                         count = 1,
#                         crs = UAV_image.crs,
#                         transform = UAV_image.transform, 
#                         dtypes = UAV_image.dtypes,
#                         dtype = UAV_image.dtypes)

show(UAV_image)
# new_tif.write(result, 1) #result from calculations
UAV_image.close()
# new_tif.close()