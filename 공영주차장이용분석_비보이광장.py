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

daily_data['Date'] = pd.to_datetime(daily_data['Date'], format='%Y-%m-%d')

daily_data.set_index('Date', drop=True, inplace=True)
#%%
'''
# 오류 발생...
# stats model의 Seasnonl_decompose 라이브러리를 활용하여 전력 수요 데이터 분해 실시 
from statsmodels.tsa.seasonal import seasonal_decompose # 데이터 필터 라이러리 호출 

result = seasonal_decompose(daily_data, model='Additive')  
result.plot()
rnt
'''
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


monthly_data['Date'] = pd.to_datetime(monthly_data['Date'])

monthly_data.set_index('Date', drop=True, inplace=True)
#%%
plt.title('비보이 광장 월별 그래프')
plt.plot(monthly_data)
#%%
'''
시계열 분해는 f5를 하게되면 오류가 발생...
# stats model의 Seasnonl_decompose 라이브러리를 활용하여 전력 수요 데이터 분해 실시 
from statsmodels.tsa.seasonal import seasonal_decompose # 데이터 필터 라이러리 호출 

result = seasonal_decompose(monthly_data, model='Additive')  
result.plot()
#%%
'''
'''
===============================================================================
월 별 진입차량수 시계열 데이터 시계열 분해 

생각해보면 daily_data를 사용하면 안됨  - 시간데이터가 손실
===============================================================================
'''
#daily_data['요일'] = daily_data['Date'].dt.day_name()

array_day = data['입차일자'].unique()

# 모든 날짜의 시간대의 값을 가진 변수
all_time_data = []
times = [i for i in range(24)]
for day in tqdm(array_day, desc = "일 별 시간대에 대한 데이터 처리중") :
    for time in times :
        temp = len(data[(data['입차일자'] == day) & (data['전처리_입차시간'] == time)])
        all_time_data.append(temp)
#%%
# 2020년 1월 1일은 수요일이니 수- 일, 월 - 일까지는 명시해주기

plt.figure(figsize=(300, 15))


plt.plot(all_time_data)
#plt.xticks(x_axis, label_x_axis)
# plt.axhline(y=sum(month_time_list) / 24, color='r', linestyle = "--", linewidth=2)
plt.xlabel('월')
plt.ylabel('진입차량수 ')
plt.title('비보이 광장 전체 진입차량수 현황')
plt.show()

#%%
array_day_with_time = []

for day in array_day :
    for time in times :
        temp = day + " " + str(time) + ":00:00"
        array_day_with_time.append(temp)
#%%
temp = {'Date' : array_day_with_time, '진입차량수' : all_time_data}
time_daily_data = pd.DataFrame(temp, columns = ['Date','진입차량수'])
time_daily_data['Date'] = pd.to_datetime(time_daily_data['Date'])
time_daily_data['요일'] = time_daily_data['Date'].dt.day_name()
time_daily_data['시간'] = time_daily_data['Date'].dt.hour
time_daily_data.set_index('Date', drop=True, inplace=True)
#%%
'''
시계열 분해는 f5를 하게되면 오류가 발생...
from statsmodels.tsa.seasonal import seasonal_decompose # 데이터 필터 라이러리 호출 

result = seasonal_decompose(time_daily_data['진입차량수'], model='Additive')  
result.plot()
'''
#%%
# 그래프가 너무 길어서 2020년 1~6월 / 2020년 7월~12월 / 2021년 1월~6월 / 2021년 7월~12일
# 2020년 1월 1일 ~ 2020년 6월 30일 : 182일 -> 4368 -> 0 ~ 4367
# 2020년 7월 1일 ~ 2020년 12월 31일 : 184일 -> 4416 -> 4368 ~ 8783
# 2021년 1월 1일 ~ 2021년 6월 30일 : 181일 -> 4344 -> 8784 ~ 13127
# 2021년 7월 1일 ~ 2021년 12월 31일 : 184일 -> 4416 -> 13128 ~ 17543
'''
===============================================================================
요일 별 진입차량수 시계열 데이터 시계열 분해 
===============================================================================
'''
num_mon = len(time_daily_data[time_daily_data['요일'] == 'Monday'] == True) / 24
num_tues = len(time_daily_data[time_daily_data['요일'] == 'Tuesday'] == True) / 24
num_wedn = len(time_daily_data[time_daily_data['요일'] == 'Wednesday'] == True) / 24
num_thurs = len(time_daily_data[time_daily_data['요일'] == 'Thursday'] == True) / 24
num_fri = len(time_daily_data[time_daily_data['요일'] == 'Friday'] == True) / 24
num_sat = len(time_daily_data[time_daily_data['요일'] == 'Saturday'] == True) / 24
num_sun = len(time_daily_data[time_daily_data['요일'] == 'Sunday'] == True) / 24

# 월 104 / 화 104 / 수 105 / 목 105 / 금 105 / 토 104 / 일 104

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
times = [i for i in range(24)]

# 나중에 plot을 그리기 위한 전체 리스트
all_day_time_list = []

for day in days :
    if day in ['Monday', 'Tuesday', 'Saturday', 'Sunday'] :
        num_of_days = 104
    elif day in ['Wednesday', 'Thrusday', 'Friday'] :
        num_of_days = 105 
        
    for time in times :
        globals()["{}_{}".format(day, time)] = sum(time_daily_data.loc[(time_daily_data['요일'] == day) &
                                                                        (time_daily_data['시간'] == time), '진입차량수'])
        exec("{}_{} = {}_{} // num_of_days".format(day, time, day, time))
        exec("all_day_time_list.append({}_{})".format(day, time))
#%%
x_axis = [24 * i for i in range(7)]
label_x_axis = ['월', '화', '수', '목', '금', '토', '일']
plt.xticks(x_axis, label_x_axis)
plt.plot(all_day_time_list)
#%%
# 전체를 뽑아봤으니 이제 요일 벼로 한 번 확인해보기
for day in days :
    temp_list = []
    for time in times :
        exec("temp_list.append({}_{})".format(day, time))
    plt.figure(figsize=(8, 6))
    x_axis = [i for i in range(24)]
    label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
    plt.plot(x_axis, temp_list)
    plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=9, width = 2,  color='r', labelrotation = 50)
    plt.axhline(y=sum(temp_list) / 24, color='r', linestyle = "--", linewidth=2)
    plt.xticks(x_axis, label_x_axis)
    plt.title('비보이 광장 주차장 {} 시간대별 그래프'.format(day))
    plt.show()
