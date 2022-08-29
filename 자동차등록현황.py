# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
#%%
# 버스 이용률 시각화
# 데이터 제공 : 전주시 버스 정책과

data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/자동차등록현황/자동차_등록_현황_20220815195606.csv', encoding='CP949')

need_columns = ['차종별', '항목', '2016', '2017', '2018', '2019', '2020', '2021.10']
data_junju = data.loc[:, need_columns]

years = ['2016', '2017', '2018', '2019', '2020', '2021.10']

num_of_car_registration = []


# 승용차만 왜냐하면 버스랑 비교할테니깐
for year in years :
    temp = data.loc[(data['항목'] == '자가용 (대)') & (data['차종별'] == '승용차'), year]
    num_of_car_registration.append(temp.iloc[0])
#%%
print(num_of_car_registration)
#%%
# 그래프 그리기
plt.figure(figsize=(10,8))
x_axis = [i for i in range(6)]
plt.plot(x_axis, num_of_car_registration, color = 'red', marker = "*")
plt.xticks(x_axis, years)
plt.xlabel('연도')
plt.ylabel('자동차 등록 대수 ')
plt.title('전주시 연도별 자동차 등록대수 현황')
plt.show()
#%%
