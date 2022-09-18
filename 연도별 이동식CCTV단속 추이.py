# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
#%%
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
#%%

# 불법 주정차 현황
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차 단속현황_20220830.csv', encoding = 'CP949')


# 데이터 날짜 전처리
data['단속일자'] = pd.to_datetime(data["단속일자"])
data['년'] =data['단속일자'].dt.year


data_2018 = len(data.loc[(data['년'] == 2018) & ((data['단속구분'] == "고정식CCTV") | (data['단속구분'] == "고정형CCTV단속")) ])
data_2019 =len( data.loc[(data['년'] == 2019) & ((data['단속구분'] == "고정식CCTV") | (data['단속구분'] == "고정형CCTV단속"))])
data_2020 = len(data.loc[(data['년'] == 2020) & ((data['단속구분'] == "고정식CCTV") | (data['단속구분'] == "고정형CCTV단속"))])
data_2021 = len(data.loc[(data['년'] == 2021) & ((data['단속구분'] == "고정식CCTV") | (data['단속구분'] == "고정형CCTV단속"))])

'''
data_2018 = len(data.loc[(data['년'] == 2018) & (data['단속구분'] == "이동식CCTV")])
data_2019 =len( data.loc[(data['년'] == 2019) & (data['단속구분'] == "이동식CCTV")])
data_2020 = len(data.loc[(data['년'] == 2020) & (data['단속구분'] == "이동식CCTV")])
data_2021 = len(data.loc[(data['년'] == 2021) & (data['단속구분'] == "이동식CCTV")])
'''


temp_list = [data_2018, data_2019, data_2020, data_2021]

plt.figure(figsize=(8, 6))
x_axis = [i for i in range(4)]
label_x_axis = [str(i) +'년' for i in range(2018, 2022)]
plt.plot(x_axis, temp_list)
#plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
#plt.axhline(y=sum(temp_list) / 24, color='r', linestyle = "--", linewidth=2)
plt.xticks(x_axis, label_x_axis)
plt.xlabel('연도')
plt.ylabel('단속 건수')
plt.title('전주시 고정식CCTV 단속 연도별 그래프')
plt.show()



