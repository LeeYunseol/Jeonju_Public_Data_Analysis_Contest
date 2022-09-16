import geopy
import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm
#%%
# 주소를 위도 경도로 바꾸는 함수 선언
def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
    return crd
#%%
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차단속카메라현황.csv')
print(data.info())
print(data.columns)
#%%
#데이터의 좌표주소 열을 이용해 지오코딩
for i, loc in tqdm(enumerate(data['주  소']), desc = "CCTV 위도 경도 전처리중"):
    temp_list = loc.split()
    address = ""
    # 만약에 한 단어라면 그 단어로만 조회
    if len(temp_list) == 1 :
        address = temp_list[0]
    # 두 글자 이상이라면
    if len(temp_list) > 1 :
        address = " ".join(temp_list[:2]) 
    # 만약에 두 글자로도 조회가 되지 않는다고 하면 신주소가 아닌 그냥 주소의 앞에 두 글자로 조회해야 함
    # try & catch 사용 
    try : 
        coord = geocoding(address)
    except AttributeError :
        temp_loc = data.loc[i, "신주소"]
        temp_list = temp_loc.split()
        address = " ".join(temp_list[:2])
        coord = geocoding(address)
        
    data.loc[i, '위도'] = coord['lat']
    data.loc[i, '경도'] = coord['lng']
#%%
data.to_csv('cctv데이터(경도위도포함).csv', encoding='CP949', index = False)