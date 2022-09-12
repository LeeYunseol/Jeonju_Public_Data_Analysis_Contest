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
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차 단속현황_20220830.csv', encoding='CP949')
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
# 불법주정차 단속유형 확인
print(data['단속구분'].unique())
print(data['단속구분'].value_counts())
#%%
'''
===============================================================================
완산구 이동식 CCTV 차량 분석
===============================================================================
'''
data_wansan = data.loc[(data['단속구분'] == "이동식CCTV") & (data['구청구분'] == "완산구") , :]

years = [2018, 2019, 2020, 2021]

for year in tqdm(years, desc = "연도별 완산구 데이터 처리중") :
    globals()['data_wansan_{}'.format(year)] =  data_wansan[data_wansan['년'] == year]
    exec("data_wansan_{} = data_wansan_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("temp = data_wansan_{}.copy()".format(year)) 
    exec("len_data = len(data_wansan_{})".format(year))
    for i in range(24) :
        globals()['interval_{}_{}_{}'.format(year, i,i+1)] =  0
    for i in tqdm(range(len_data), desc = "{}별 시간대 별 단속 건수 전처리중".format(year)) :
        exec('interval_{}_{}_{} += 1'.format(year, int(temp.loc[i, '단속된 시간']), int(temp.loc[i, '단속된 시간'])+1))
    time_list = []
    for i in range(24) :
        exec('time_list.append(interval_{}_{}_{})'.format(year, i, i+1))
    # 그래프 그리기
    plt.figure(figsize=(8,6))
    x_axis = [i for i in range(24)]
    label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
    plt.plot(x_axis, time_list, marker = '*')
    plt.xticks(x_axis, label_x_axis)
    plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
    plt.axhline(y=sum(time_list) / 24, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('시간')
    plt.ylabel('불법주정차 단속 수 ')
    plt.title('완산구 {}년 시간별 이동식 CCTV 불법주정차 현황'.format(year))
    plt.show()
#%%
# 완산구 위치별 불법주정차 단속 현황
# 할게 없네?
#%%
'''
===============================================================================
덕진구 이동식 CCTV 차량 분석
===============================================================================
'''
data_dukjin = data.loc[(data['단속구분'] == "이동식CCTV") & (data['구청구분'] == "덕진구") , :]

years = [2018, 2019, 2020, 2021]

for year in tqdm(years, desc = "연도별 완산구 데이터 처리중") :
    globals()['data_dukjin_{}'.format(year)] =  data_dukjin[data_dukjin['년'] == year]
    exec("data_dukjin_{} = data_dukjin_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("temp = data_dukjin_{}.copy()".format(year)) 
    exec("len_data = len(data_dukjin_{})".format(year))
    for i in range(24) :
        globals()['interval_{}_{}_{}'.format(year, i,i+1)] =  0
    for i in tqdm(range(len_data), desc = "{}별 시간대 별 단속 건수 전처리중".format(year)) :
        exec('interval_{}_{}_{} += 1'.format(year, int(temp.loc[i, '단속된 시간']), int(temp.loc[i, '단속된 시간'])+1))
    time_list = []
    for i in range(24) :
        exec('time_list.append(interval_{}_{}_{})'.format(year, i, i+1))
    # 그래프 그리기
    plt.figure(figsize=(8,6))
    x_axis = [i for i in range(24)]
    label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
    plt.plot(x_axis, time_list, marker = '*')
    plt.xticks(x_axis, label_x_axis)
    plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
    plt.axhline(y=sum(time_list) / 24, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('시간')
    plt.ylabel('불법주정차 단속 수 ')
    plt.title('덕진구 {}년 시간별 이동식 CCTV 불법주정차 현황'.format(year))
    plt.show()
#%%
print(data_wansan['단속된 시간'].value_counts())
#%%
data.to_csv('전처리된 불법주정차현황.csv', index = False, encoding = 'CP949')