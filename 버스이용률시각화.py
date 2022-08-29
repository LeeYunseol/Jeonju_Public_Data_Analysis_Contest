# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
#%%
# 버스 이용률 시각화
# 데이터 제공 : 전주시 버스 정책과

data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/버스이용률.csv', encoding='utf-8')
data.info()
#%%
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
#%%
# 승차인원 ',' 전처리하기 : object -> int

for i in tqdm(range(len(data)), desc = "승차인원 object -> int 데이터 전처리 중") :
    temp = data.loc[i, '승차인원']
    temp_list = temp.split(',')
    temp_num = int(temp_list[0] + temp_list[1])
    data.loc[i, '승차인원'] = temp_num
#%%
'''
===============================================================================
버스 이용률 시각화 
===============================================================================
'''

# 코로나 발생은 2019년 12월 31일 -> 2019년 & 2020년 비교, 2019년 & 2021년 비교, 2019년 & 2022년 비교


total_2019 = sum(data.loc[(data['연도'] == 2019), '승차인원'])
total_2020 = sum(data.loc[(data['연도'] == 2020), '승차인원'])
total_2021 = sum(data.loc[(data['연도'] == 2021), '승차인원'])
total_2019_6 = sum(data.loc[(data['연도'] == 2019) &
                            ((data['월'] == 1) | (data['월'] == 2) | (data['월'] == 3) | (data['월'] == 4) | (data['월'] == 5) | (data['월'] == 6)), '승차인원'])
total_2022_6 = sum(data.loc[(data['연도'] == 2022) &
                            ((data['월'] == 1) | (data['월'] == 2) | (data['월'] == 3) | (data['월'] == 4) | (data['월'] == 5) | (data['월'] == 6)), '승차인원'])

# 2019 - 2020 - 2021 전체 버스 이용률 꺾은선 그래프
plt.figure(figsize=(10,8))
x_axis = [0,1,2]
label_x_axis = ['2019', '2020', '2021']
plt.plot(x_axis, [total_2019, total_2020, total_2021], marker = "*")
plt.axvline(x=0.5, color='r', linestyle='--', linewidth=3)
plt.xticks(x_axis, label_x_axis)
plt.title('연도별 버스 이용률')
plt.show()
#%%
# 2019년 6월까지의 데이터와 2022년 6월까지의 데이터 비교하기
plt.figure(figsize=(10,8))
x_axis = [0,1]
label_x_axis = ['2019년 6월까지', '2022년 6월까지']
plt.plot(x_axis, [total_2019_6, total_2022_6], marker = "*")
plt.axvline(x=0.5, color='r', linestyle='--', linewidth=3)
plt.xticks(x_axis, label_x_axis)
plt.title('연도별 버스 이용률')
plt.show()
#%%
# 2019 & 2020 & 2021 & 2022년 6월까지의 데이터 비교하기
#%%
# 월 별로 데이터 분석해보기
years = [2019, 2020, 2021, 2022]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

month_2019 = []
month_2020 = []
month_2021 = []
month_2022 = []
for year in years :
    for month in months :
        if(year == 2022 and month == 7) :
            break
        temp = data.loc[(data['연도'] ==year) & (data['월'] == month), '승차인원']
        exec("month_{}.append(temp)".format(year))

# 2019 - 2020 - 2021 - 2022 월 별로 데이터 시각화
plt.figure(figsize=(10,8))
x_axis = [i for i in range(12)]
label_x_axis = [str(i) + '월' for i in range(12)]
plt.xticks(x_axis, label_x_axis)
plt.plot(x_axis, month_2019, color = 'red', label = '2019', marker = "*")
plt.plot(x_axis, month_2020, color = 'blue', label = '2020', marker = "*")
plt.plot(x_axis, month_2021, color = 'green', label = '2021', marker = "*")
plt.plot([0, 1, 2, 3, 4, 5], month_2022, color = 'violet', label = '2022', marker = "*")
plt.title('월별 버스 이용률')
plt.legend()
plt.show()
#%%
