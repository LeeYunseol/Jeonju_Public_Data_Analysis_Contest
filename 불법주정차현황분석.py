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
# ★★★★★★★ 나중에 해볼 것 : 2018~2021데이터를 다 통합해서 시계열 분해 
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차 단속현황_20220820.csv', encoding='CP949')

# 0시와 23시에도 단속을 한 적이 있음
# 덕진구 : 2017년 상반기부터 2022년 상반기  478867개
# 완산구 : 2017년 하반기부터 2022년 상반기 469709개
# 데이터가 온전하게 있는 2018년~2021년부터 분석 후에 2022년 예상을 하는 것도 좋을 것 같음


# 데이터 날짜 전처리
data['단속일자'] = pd.to_datetime(data["단속일자"])
data['년'] =data['단속일자'].dt.year
data['월'] =data['단속일자'].dt.month 
data['일'] = data['단속일자'].dt.day

for i in tqdm(range(len(data)), desc = "단속 시간 전처리중") :
    temp = data.loc[i, '단속시간']
    temp2 = temp.split(":")
    time = int(temp2[0])
    data.loc[i, '단속된 시간'] = time
#%%
'''
===============================================================================
덕진구
===============================================================================
'''

data_dukjin = data[data['구청구분'] == '덕진구'] 

years = [2018, 2019, 2020, 2021]

data_dukjin_2020 = data_dukjin[data_dukjin['년'] == 2020]
data_dukjin_2020 = data_dukjin_2020.reset_index(inplace = False, drop = True)
for i in range(24) :
    globals()['interval_{}_{}'.format(i,i+1)] =  0
    
for i in tqdm(range(len(data_dukjin_2020)), desc = "시간대 별 단속 건수 전처리중") :
    exec('interval_{}_{} += 1'.format(int(data_dukjin_2020.loc[i, '단속된 시간']), int(data_dukjin_2020.loc[i, '단속된 시간'])+1))
    
time_list = []
for i in range(24) :
    exec('time_list.append(interval_{}_{})'.format(i, i+1))
#%%
# 2020년 시간별 불법 주차 현황 그래프 그리기
plt.figure(figsize=(8,6))
'''
막대그래프 그릴때
x_axis = [i for i in range(1, 25)]
y_interval = [i+0.5 for i in range(24)]
plt.bar(y_interval, time_list)
'''
x_axis = [i for i in range(24)]
label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
plt.plot(x_axis, time_list, marker = '*')
plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
plt.axhline(y=sum(time_list) / 24, color='r', linestyle = "--", linewidth=2)
plt.xlabel('시간')
plt.ylabel('불법주정차 단속 수 ')
plt.title('덕진구 2020년 불법주정차 현황')
plt.show()