# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
#%%
# 비보이광장 주차장 분석   124대주차가능 
# 완산구 위치
# 연도 별로(2020/ 2021) 나누고 시간 / 월 별로 나눠서 시계열 분석해보기
# ★ 전화 통화해서 확인한 결과, 서부신 시가지 비보이광장 주차장은 만석 시에 입구에서 통제를 못함 -> 그래서 회차 데이터 발생
# ★★★ 비보이 광장 데이터는 실내 주차장 데이터와 다르게 일 별 데이터가 존재함, 이를 활용하면 좋은 자료가 될 것임
'''
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_공영주차장 이용 내역(서부신시가지 비보이광장).csv', encoding='CP949')
data.info()
#%%
# 출차 처리 중에 출차완료만 된 것을 사용 -> 사전 정산이 있는데 이는 출차 시간을 파악할 수 없음

data = data[data['출차처리'] == '출차완료']
data.reset_index(drop=True, inplace = True)
#%%

===============================================================================
입차일자 & 출차일자 처리
===============================================================================


for i in tqdm(range(len(data)), desc = "시간 전처리중") :
    temp_entry = data.loc[i, '입차시간'].split(":")
    temp_exit = data.loc[i, '출차시간'].split(":")
    
    data.loc[i, '전처리_입차시간'] = int(temp_entry[0])
    data.loc[i, '전처리_출차시간'] = int(temp_exit[0])
    
data['입차일자'] = pd.to_datetime(data["입차일자"])
data['입차일자_년'] =data['입차일자'].dt.year
data['입차일자_월'] =data['입차일자'].dt.month 
data['입차일자_일'] = data['입차일자'].dt.day

data['출차일자'] = pd.to_datetime(data["출차일자"])
data['출차일자_년'] =data['출차일자'].dt.year
data['출차일자_월'] =data['출차일자'].dt.month 
data['출차일자_일'] = data['출차일자'].dt.day


data.to_csv('전처리된 비보이광장 데이터.csv', index = None, encoding='CP949')
'''

data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전처리된 비보이광장 데이터.csv', encoding='CP949')
#%%
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

data.info()
#%%
'''
===============================================================================
데이터 통합 전처리
동일 년도 - 월
2020 - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 월 - 시간
2021 - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 월 - 시간
===============================================================================
'''
years = [2020, 2021]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for year in years :
    globals()['entry_data_{}'.format(year)] =  data[data['입차일자_년'] == year]
    globals()['exit_data_{}'.format(year)] =  data[data['출차일자_년'] == year]
    
    exec("entry_data_{} = entry_data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("exit_data_{} = exit_data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    
    exec("temp_entry = entry_data_{}.copy()".format(year)) 
    exec("temp_exit = exit_data_{}.copy()".format(year))
    
    for month in months :
        entry_month_time_list = []
        exit_month_time_list = []
        for time in range(24) :
            globals()['entry_data_{}_{}_{}'.format(year, time, time+1)] = len(temp_entry[(temp_entry['입차일자_월'] == month) & (temp_entry['전처리_입차시간'] == time)])
            
                                                              
            
            globals()['exit_data_{}_{}_{}'.format(year, time, time+1)] = len(temp_exit[(temp_exit['출차일자_월'] == month) & (temp_exit['전처리_출차시간'] == time)])
                                                                        
            
            entry_month_time_list.append(globals()['entry_data_{}_{}_{}'.format(year, time, time+1)])
            exit_month_time_list.append(globals()['exit_data_{}_{}_{}'.format(year, time, time+1)])
        # 진입차량 그래프 그리기
        plt.figure(figsize=(10,8))
        x_axis = [i for i in range(24)]
        label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
        plt.plot(x_axis, entry_month_time_list, marker = '*')
        plt.xticks(x_axis, label_x_axis)
        plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
        # plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
        plt.xlabel('시간')
        plt.ylabel('진입차량수 ')
        plt.title('비보이 광장 {}년 {}월 시간별 진입차량수 현황'.format(year, month))
        plt.show()
        
        # 진츨차량 그래프 그리기
        plt.figure(figsize=(10,8))
        x_axis = [i for i in range(24)]
        label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
        plt.plot(x_axis, exit_month_time_list, marker = '*')
        plt.xticks(x_axis, label_x_axis)
        plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
        # plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
        plt.xlabel('시간')
        plt.ylabel('진출차량수 ')
        plt.title('비보이 광장 {}년 {}월 시간별 진출차량수 현황'.format(year, month))
        plt.show()
        
#%%
'''
===============================================================================
데이터 통합 전처리
2020 - 시간
2021 - 시간
===============================================================================
'''
years = [2020, 2021]

for year in years :
    globals()['entry_data_{}'.format(year)] =  data[data['입차일자_년'] == year]
    globals()['exit_data_{}'.format(year)] =  data[data['출차일자_년'] == year]
    
    exec("entry_data_{} = entry_data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("exit_data_{} = exit_data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    
    exec("temp_entry = entry_data_{}.copy()".format(year)) 
    exec("temp_exit = exit_data_{}.copy()".format(year))
    
    entry_month_time_list = []
    exit_month_time_list = []
    for time in range(24) :
        globals()['entry_data_{}_{}_{}'.format(year, time, time+1)] = len(temp_entry[(temp_entry['전처리_입차시간'] == time)])
        globals()['exit_data_{}_{}_{}'.format(year, time, time+1)] = len(temp_exit[(temp_exit['전처리_출차시간'] == time)])
                                                                    
        entry_month_time_list.append(globals()['entry_data_{}_{}_{}'.format(year, time, time+1)])
        exit_month_time_list.append(globals()['exit_data_{}_{}_{}'.format(year, time, time+1)])
    exec("total_entry_{} = entry_month_time_list".format(year))
    exec("total_exit_{} = exit_month_time_list".format(year))
    # 진입차량 그래프 그리기
    plt.figure(figsize=(10,8))
    x_axis = [i for i in range(24)]
    label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
    plt.plot(x_axis, entry_month_time_list, marker = '*')
    plt.xticks(x_axis, label_x_axis)
    plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
    # plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('시간')
    plt.ylabel('진입차량수 ')
    plt.title('비보이 광장 {}년 시간별 진입차량수 현황'.format(year))
    plt.show()
    
    # 진츨차량 그래프 그리기
    plt.figure(figsize=(10,8))
    x_axis = [i for i in range(24)]
    label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
    plt.plot(x_axis, exit_month_time_list, marker = '*')
    plt.xticks(x_axis, label_x_axis)
    plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
    # plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('시간')
    plt.ylabel('진출차량수 ')
    plt.title('비보이 광장 {}년 시간별 진출차량수 현황'.format(year))
    plt.show()
#%%
# 2020년 & 2021년 데이터 같이 그리기

plt.figure(figsize=(10,8))
x_axis = [i for i in range(24)]
label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
plt.plot(x_axis, total_entry_2020, color= 'red', marker = '*', label = '2020')
plt.plot(x_axis, total_entry_2021, color = 'blue', marker='*', label = '2021')
plt.xticks(x_axis, label_x_axis)
# plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
plt.xlabel('월')
plt.ylabel('진입차량수 ')
plt.title('비보이 광장 2020 & 2021년 전체 시간별 진입차량수 현황')
plt.legend()
plt.show()

plt.figure(figsize=(10,8))
x_axis = [i for i in range(24)]
label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
plt.plot(x_axis, total_exit_2020, color= 'red', marker = '*', label = '2020')
plt.plot(x_axis, total_exit_2021, color = 'blue', marker='*', label = '2021')
plt.xticks(x_axis, label_x_axis)
# plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
plt.xlabel('월')
plt.ylabel('진출차량수 ')
plt.title('비보이 광장 2020 & 2021년 전체 시간별 진출차량수 현황')
plt.legend()
plt.show()

#%%
'''
===============================================================================
데이터 통합 전처리
2020 - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 월
2021 - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 월 
===============================================================================
'''

years = [2020, 2021]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for year in years :
    globals()['entry_data_{}'.format(year)] =  data[data['입차일자_년'] == year]
    globals()['exit_data_{}'.format(year)] =  data[data['출차일자_년'] == year]
    
    exec("entry_data_{} = entry_data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    exec("exit_data_{} = exit_data_{}.reset_index(inplace = False, drop = True)".format(year, year))
    
    exec("temp_entry = entry_data_{}.copy()".format(year)) 
    exec("temp_exit = exit_data_{}.copy()".format(year))
    
    globals()["total_entry_{}".format(year)] = [0 for i in range(12)]
    globals()["total_exit_{}".format(year)] = [0 for i in range(12)]
    
    entry_month_time_list = []
    exit_month_time_list = []
    
    for month in months :
        
        
        globals()['entry_data_{}_{}'.format(year, month)] = len(temp_entry.loc[(temp_entry['입차일자_월'] == month)])
        globals()['exit_data_{}_{}'.format(year, month)] = len(temp_exit[(temp_exit['출차일자_월'] == month)])
                                                                    
        entry_month_time_list.append(globals()['entry_data_{}_{}'.format(year, month)])
        exit_month_time_list.append(globals()['exit_data_{}_{}'.format(year, month)])
        
    globals()["total_entry_{}".format(year)] = [globals()["total_entry_{}".format(year)][i] + entry_month_time_list[i] for i in range(12)]
    globals()["total_exit_{}".format(year)] = [globals()["total_exit_{}".format(year)][i] + exit_month_time_list[i] for i in range(12)]
    
    # 진입차량 그래프 그리기
    plt.figure(figsize=(10,8))
    x_axis = [i for i in range(12)]
    label_x_axis = [str(i) + '월' for i in range(12)]
    exec("plt.plot(x_axis, total_entry_{}, marker = '*')".format(year))
    plt.xticks(x_axis, label_x_axis)
    # plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('월')
    plt.ylabel('진입차량수 ')
    plt.title('비보이 광장 {}년 전체 월별 진입차량수 현황'.format(year, month))
    plt.show()
    
    # 진츨차량 그래프 그리기
    plt.figure(figsize=(10,8))
    x_axis = [i for i in range(12)]
    label_x_axis = [str(i) + '월' for i in range(12)]
    exec("plt.plot(x_axis, total_exit_{}, marker = '*')".format(year))
    plt.xticks(x_axis, label_x_axis)
    # plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
    plt.xlabel('월')
    plt.ylabel('진출차량수 ')
    plt.title('비보이 광장 {}년 전체 월별 진출차량수 현황'.format(year, month))
    plt.show()
    
#%%
# 2020년 & 2021년 데이터 같이 그리기

plt.figure(figsize=(10,8))
x_axis = [i for i in range(12)]
label_x_axis = [str(i) + '월' for i in range(12)]
plt.plot(x_axis, total_entry_2020, color= 'red', marker = '*', label = '2020')
plt.plot(x_axis, total_entry_2021, color = 'blue', marker='*', label = '2021')
plt.xticks(x_axis, label_x_axis)
# plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
plt.xlabel('월')
plt.ylabel('진입차량수 ')
plt.title('비보이 광장 2020 & 2021년 전체 월별 진입차량수 현황')
plt.legend()
plt.show()

plt.figure(figsize=(10,8))
x_axis = [i for i in range(12)]
label_x_axis = [str(i) + '월' for i in range(12)]
plt.plot(x_axis, total_exit_2020, color= 'red', marker = '*', label = '2020')
plt.plot(x_axis, total_exit_2021, color = 'blue', marker='*', label = '2021')
plt.xticks(x_axis, label_x_axis)
# plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
plt.xlabel('월')
plt.ylabel('진출차량수 ')
plt.title('비보이 광장 2020 & 2021년 전체 월별 진출차량수 현황')
plt.legend()
plt.show()

#%%
'''
===============================================================================
일 별 시계열 진입차량수 데이터 시계열 분해 
===============================================================================
'''
daily_data = data['입차일자'].value_counts(sort=False)
#plt.plot(daily_data)

#시리즈를 데이터프레임으로
daily_data = pd.DataFrame(daily_data, columns=['입차일자'])
daily_data.reset_index(inplace = True)
daily_data.rename(columns={'index':'Date'}, inplace=True)
daily_data.sort_index(inplace=True)
#%%
daily_data.info()

daily_data['Date'] = pd.to_datetime(daily_data['Date'])

daily_data.set_index('Date', drop=True, inplace=True)
#%%
# stats model의 Seasnonl_decompose 라이브러리를 활용하여 전력 수요 데이터 분해 실시 
from statsmodels.tsa.seasonal import seasonal_decompose # 데이터 필터 라이러리 호출 

result = seasonal_decompose(daily_data, model='Additive')  
result.plot()

#%%
'''
===============================================================================
월 별 진입차량수 시계열 데이터 시계열 분해 
===============================================================================
'''

# 월별 데이터를 모아야하기 때문에 년도-월로 데이터를 통합
for i in tqdm(range(len(data)), desc = "년-월 데이터 전처리중") :
    data.loc[i, '입차일자_년_월'] = str(data.loc[i, '입차일자_년']) + "-" + str(data.loc[i, '입차일자_월'])
#%%
monthly_data = data['입차일자_년_월'].value_counts(sort=False)


#시리즈를 데이터프레임으로
monthly_data = pd.DataFrame(monthly_data, columns=['입차일자_년_월'])
monthly_data.reset_index(inplace = True)
monthly_data.rename(columns={'index':'Date'}, inplace=True)
monthly_data.sort_index(inplace=True)

monthly_data.info()

monthly_data['Date'] = pd.to_datetime(monthly_data['Date'])

monthly_data.set_index('Date', drop=True, inplace=True)
#%%
plt.title('비보이 광장 월별 그래프')
plt.plot(monthly_data)
#%%
# stats model의 Seasnonl_decompose 라이브러리를 활용하여 전력 수요 데이터 분해 실시 
from statsmodels.tsa.seasonal import seasonal_decompose # 데이터 필터 라이러리 호출 

result = seasonal_decompose(monthly_data, model='Additive')  
result.plot()
