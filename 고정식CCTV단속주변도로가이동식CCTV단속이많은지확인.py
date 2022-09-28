# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
#%%
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
#%%
# 불법 주정차 단속현황 불러오기
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전처리된 불법주정차현황.csv', encoding='CP949')
#%%
# 단속 장소 명시를 다 통일했는지 아니면 다르게 했는지
temp_data = data.loc[(data["단속구분"] == "이동식CCTV"), :]
temp = temp_data['단속된 시간'].value_counts()
#%%
'''
===============================================================================
덕진구 고정식 CCTV 단속이 많은 곳 주변 도로에 이동식 CCTV 단속이 많은지 확인하기
===============================================================================
'''
# 먼저 덕진구에 고정식 CCTV 단속이 많은 곳 확인하기
data_dukjin = data.loc[(data['단속구분'] == "고정식CCTV") & (data['구청구분'] == "덕진구") & (data['단속된 시간'] == 10), :]
data_dukjin_place = data_dukjin['단속장소명'].value_counts()
#%%
# 주변 도로 확인
data_cctv_move = data.loc[(data['단속구분'] == "이동식CCTV") & (data['구청구분'] == "덕진구") & (data['단속된 시간'] == 10), :]
data_cctv_move_place = data_cctv_move['단속장소명'].value_counts()
#%%
# 박스플롯
plt.boxplot(data_cctv_move_place)
plt.show()
#%%
# 히스토그램
sns.distplot(data_cctv_move_place)
plt.show()
#%%
print(sum(data_cctv_move_place[0:19]))
print(sum(data_cctv_move_place[0:19]) / sum(data_cctv_move_place) * 100)
#%%
# 덕진구 고정식 cctv 단속된 구간의 중위수와 4 사분위 비교하기
q3 = data_dukjin_place.quantile(0.5) # 84.5 => 파인트리몰
q4 = data_dukjin_place.quantile(0.8) # 515.75 => 롯데마트 주차장 입구 or 모래내시장 주차장입구
num = 0
for i in list(list(data_cctv_move_place.index)) :
    if '온고올로' in i :
        print(num)
    num += 1
print(data_cctv_move_place.iloc[38])
#%%
'''
===============================================================================
완산구 고정식 CCTV 단속이 많은 곳 주변 도로에 이동식 CCTV 단속이 많은지 확인하기
===============================================================================
'''
# 먼저 덕진구에 고정식 CCTV 단속이 많은 곳 확인하기
data_wansan = data.loc[(data['단속구분'] == "고정형CCTV단속") & (data['구청구분'] == "완산구"), :]
data_wansan_place = data_wansan['단속장소명'].value_counts()
#%%
# 주변 도로 확인
data_cctv_move = data.loc[(data['단속구분'] == "이동식CCTV") & (data['구청구분'] == "완산구"), :]
data_cctv_move_place = data_cctv_move['단속장소명'].value_counts()

#%%
# 덕진구 고정식 cctv 단속된 구간의 중위수와 4 사분위 비교하기
q3 = data_wansan_place.quantile(0.5) #
q4 = data_wansan_place.quantile(0.75) # 688 => 오성대우아파트
num = 0
for i in list(list(data_cctv_move_place.index)) :
    if '거마산' in i :
        print(i)
    num += 1
print(data_cctv_move_place.iloc[43])
