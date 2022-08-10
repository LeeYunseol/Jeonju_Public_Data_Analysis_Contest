'''
import geopandas as gpd
import matplotlib.pyplot as plt
from pyproj import CRS
import pandas as pd

data = gpd.read_file('전주시_시군구.shp', encoding='utf-8')

data.plot()
#%%
park = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/전국주차장/전라북도_전주시_주차장정보_20220311_1647220760617_29835.csv', encoding='CP949')

# GeoDataFrame 형식으로 변환하기
park = gpd.GeoDataFrame(park, geometry=gpd.points_from_xy(park['경도'], park['위도']))
type(park)  # geopandas.geodataframe.GeoDataFrame

park.set_crs(epsg = 4326, inplace = True)



base = data.plot(color='white', edgecolor="k")
ax = park.plot(ax=base, marker='o', color='red', markersize=5)
ax.set_axis_off()
ax.set_title("세계 도시 분포")
plt.show()
'''
