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
연도별 덕진구 불법주정차 추이
===============================================================================
'''

data_dukjin = data[data['구청구분'] == '덕진구'] 

temp_list = []
years = [2018, 2019, 2020, 2021]

for year in years :
    temp = data_dukjin[data_dukjin['년'] == year]
    temp_list.append(len(temp))

# 그래프 그리기
plt.figure(figsize=(8,6))
x_axis = [i for i in range(4)]
label_x_axis = [str(i) + '년' for i in range(2018, 2022)]
plt.plot(x_axis, temp_list, marker = '*')
plt.xticks(x_axis, label_x_axis)
plt.xlabel('연도')
plt.ylabel('불법주정차 단속 수 ')
plt.title('덕진구 불법주정차 현황')
plt.show()

#%%
'''
===============================================================================
연도별 완산구 불법주정차 추이
===============================================================================
'''

data_wansan = data[data['구청구분'] == '완산구'] 

temp_list = []
years = [2018, 2019, 2020, 2021]

for year in years :
    temp = data_wansan[data_wansan['년'] == year]
    temp_list.append(len(temp))

# 그래프 그리기
plt.figure(figsize=(8,6))
x_axis = [i for i in range(4)]
label_x_axis = [str(i) + '년' for i in range(2018, 2022)]
plt.plot(x_axis, temp_list, marker = '*')
plt.xticks(x_axis, label_x_axis)
plt.xlabel('연도')
plt.ylabel('불법주정차 단속 수 ')
plt.title('완산구 불법주정차 현황')
plt.show()

#%%
'''
===============================================================================
연도별 전주시 불법주정차 추이
===============================================================================
'''

temp_list = []
years = [2018, 2019, 2020, 2021]

for year in years :
    temp = data[data['년'] == year]
    temp_list.append(len(temp))

# 그래프 그리기
plt.figure(figsize=(8,6))
x_axis = [i for i in range(4)]
label_x_axis = [str(i) + '년' for i in range(2018, 2022)]
plt.plot(x_axis, temp_list, marker = '*')
plt.xticks(x_axis, label_x_axis)
plt.xlabel('연도')
plt.ylabel('불법주정차 단속 수 ')
plt.title('전주시 불법주정차 현황')
plt.show()
#%%
'''
===============================================================================
덕진구(시간별)
===============================================================================
'''

data_dukjin = data[data['구청구분'] == '덕진구'] 

years = [2018, 2019, 2020, 2021]

for year in tqdm(years, desc = "연도별 덕진구 데이터 처리중") :
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
    plt.title('덕진구 {}년 시간별 불법주정차 현황'.format(year))
    plt.show()
#%%
'''
===============================================================================
완산구(시간별)
===============================================================================
'''

data_wansan = data[data['구청구분'] == '완산구'] 

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
    plt.title('완산구 {}년 시간별 불법주정차 현황'.format(year))
    plt.show()

#%%
'''
===============================================================================
전주시(시간별)
===============================================================================
'''

years = [2018, 2019, 2020, 2021]

for year in tqdm(years, desc = "연도별 완산구 데이터 처리중") :
    globals()['data_{}'.format(year)] =  data[data['년'] == year]
    exec("data_{} = data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("temp = data_{}.copy()".format(year)) 
    exec("len_data = len(data_{})".format(year))
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
    plt.title('전주시 {}년 시간별 불법주정차 현황'.format(year))
    plt.show()

#%%
'''
===============================================================================
덕진구(월별)
===============================================================================
'''

data_dukjin = data[data['구청구분'] == '덕진구'] 

years = [2018, 2019, 2020, 2021]

for year in tqdm(years, desc = "연도별 덕진구 데이터 처리중") :
    globals()['data_dukjin_{}'.format(year)] =  data_dukjin[data_dukjin['년'] == year]
    exec("data_dukjin_{} = data_dukjin_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("temp = data_dukjin_{}.copy()".format(year)) 
    exec("len_data = len(data_dukjin_{})".format(year))
    for i in range(1, 13) :
        globals()['interval_{}_{}'.format(year, i)] =  0
    for i in tqdm(range(len_data), desc = " 덕진구 {}별 월별 단속 건수 전처리중".format(year)) :
        exec('interval_{}_{} += 1'.format(year, int(temp.loc[i, '월'])))
    time_list = []
    for i in range(1, 13) :
        exec('time_list.append(interval_{}_{})'.format(year, i))
    # 그래프 그리기
    plt.figure(figsize=(8,6))
    x_axis = [i for i in range(12)]
    label_x_axis = [str(i) + '월' for i in range(1, 13)]
    plt.plot(x_axis, time_list, marker = '*')
    plt.xticks(x_axis, label_x_axis)
    plt.axhline(y=sum(time_list) / 12, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('월')
    plt.ylabel('불법주정차 단속 수 ')
    plt.title('덕진구 {}년 월별 불법주정차 현황'.format(year))
    plt.show()
    
#%%
'''
===============================================================================
완산구(월별)
===============================================================================
'''

data_wansan = data[data['구청구분'] == '완산구'] 

years = [2018, 2019, 2020, 2021]

for year in tqdm(years, desc = "연도별 완산구 데이터 처리중") :
    globals()['data_wansan_{}'.format(year)] =  data_wansan[data_wansan['년'] == year]
    exec("data_wansan_{} = data_wansan_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("temp = data_wansan_{}.copy()".format(year)) 
    exec("len_data = len(data_wansan_{})".format(year))
    for i in range(1, 13) :
        globals()['interval_{}_{}'.format(year, i)] =  0
    for i in tqdm(range(len_data), desc = " 완산구 {}별 월별 단속 건수 전처리중".format(year)) :
        exec('interval_{}_{} += 1'.format(year, int(temp.loc[i, '월'])))
    time_list = []
    for i in range(1, 13) :
        exec('time_list.append(interval_{}_{})'.format(year, i))
    # 그래프 그리기
    plt.figure(figsize=(8,6))
    x_axis = [i for i in range(12)]
    label_x_axis = [str(i) + '월' for i in range(1, 13)]
    plt.plot(x_axis, time_list, marker = '*')
    plt.xticks(x_axis, label_x_axis)
    plt.axhline(y=sum(time_list) / 12, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('월')
    plt.ylabel('불법주정차 단속 수 ')
    plt.title('완산구 {}년 월별 불법주정차 현황'.format(year))
    plt.show()

#%%
'''
===============================================================================
전주시(월별)
===============================================================================
'''

years = [2018, 2019, 2020, 2021]

for year in tqdm(years, desc = "연도별 전주시 데이터 처리중") :
    globals()['data_{}'.format(year)] =  data[data['년'] == year]
    exec("data_{} = data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("temp = data_{}.copy()".format(year)) 
    exec("len_data = len(data_{})".format(year))
    for i in range(1, 13) :
        globals()['interval_{}_{}'.format(year, i)] =  0
    for i in tqdm(range(len_data), desc = " 전주시 {}별 월별 단속 건수 전처리중".format(year)) :
        exec('interval_{}_{} += 1'.format(year, int(temp.loc[i, '월'])))
    time_list = []
    for i in range(1, 13) :
        exec('time_list.append(interval_{}_{})'.format(year, i))
    # 그래프 그리기
    plt.figure(figsize=(8,6))
    x_axis = [i for i in range(12)]
    label_x_axis = [str(i) + '월' for i in range(1, 13)]
    plt.plot(x_axis, time_list, marker = '*')
    plt.xticks(x_axis, label_x_axis)
    plt.axhline(y=sum(time_list) / 12, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('월')
    plt.ylabel('불법주정차 단속 수 ')
    plt.title('전주시 {}년 월별 불법주정차 현황'.format(year))
    plt.show()