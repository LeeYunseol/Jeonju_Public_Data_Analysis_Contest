# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
# 실내 체육관 주차장 분석 - 요일별 분석은 불가   150대주차가능 
# 덕진구에 위치
# 연도 별로(2020/ 2021) 나누고 시간 / 월 별로 나눠서 시계열 분석해보기


# ★★★★★★★★ 주차구획수가 150대인데 진입차량수가 2000대 이상이 나올수가 있나?


data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_공영주차장 이용 통계(실내체육관).csv', encoding='CP949')

# 데이터를 활용하기 전에 진입차량수(일반) 열과 진출차량수(일반) 열은 , 때문에 object이기 때문에 전처리
columns = ['진입차량수(일반)', '진출차량수(일반)']
for column in columns :
    for i in range(len(data)) :
        temp = data.loc[i, column]
        if len(temp) >= 5 :
            temp_split = temp.split(',')
            num_temp = temp_split[0] + temp_split[1]
            data.loc[i, column] = float(num_temp)
            
        else :
            data.loc[i, column] = float(temp)
            #%%
data.info()
#%%
# 진입차량수
# 2020년 
data_2020 = data[data['연도'] == 2020]

# 2020년 주차장 데이터에서 시간별로 분석하기 위해 동일 시간대의 1~12월까지의 합을 구하고 평균을 내기
# 어차피 월 별로 다시 분석할 것이기 때문에 이렇게 해줘도 된다고 판단
entry_list_by_time_2020 = []
for i in range(24) :
    time = str(i) + ':00 ~ ' + str(i+1) + ':00'
    globals()['entry_data_2020_{}_{}'.format(i,i+1)] =  int(sum(data_2020[data_2020['시간대'] == time].loc[:, '진입차량수(일반)']) / 12)
    entry_list_by_time_2020.append(globals()['entry_data_2020_{}_{}'.format(i,i+1)])
    
#%%
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
#%%
# 2020년 시간별 그래프 그리기
plt.figure(figsize=(20,15))
x_axis = [i for i in range(24)]
label_x_axis = [str(i) + '시~'+str(i+1)+'시' for i in range(24)]
plt.bar(x_axis, entry_list_by_time_2020, color='red')
plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xlabel('시간')
plt.ylabel('진입차량수(일반)')
plt.title('2020년 실내 체육관 주차장 진입차량수(일반)')
plt.show()
#%%
# 2021년 
data_2021 = data[data['연도'] == 2021]

# 2020년 주차장 데이터에서 시간별로 분석하기 위해 동일 시간대의 1~12월까지의 합을 구하고 평균을 내기
# 어차피 월 별로 다시 분석할 것이기 때문에 이렇게 해줘도 된다고 판단
entry_list_by_time_2021 = []
for i in range(24) :
    time = str(i) + ':00 ~ ' + str(i+1) + ':00'
    globals()['entry_data_2021_{}_{}'.format(i,i+1)] =  int(sum(data_2021[data_2021['시간대'] == time].loc[:, '진입차량수(일반)']) / 12)
    entry_list_by_time_2021.append(globals()['entry_data_2021_{}_{}'.format(i,i+1)])
#%%
# 2021년 시간별 그래프 그리기
plt.figure(figsize=(20,15))
x_axis = [i for i in range(24)]
plt.bar(x_axis, entry_list_by_time_2021, color='blue')
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xticks(x_axis, label_x_axis)
plt.xlabel('시간')
plt.ylabel('진입차량수(일반)')
plt.title('2021년 실내 체육관 주차장 진입차량수(일반)')
plt.show()    
#%%
# 2020년 시간별 그래프와 2021년 시간별 그래프 같이 그리기
plt.figure(figsize=(20,15))
bar_width = 0.4
index = np.arange(24)
b1 = plt.bar(index - 0.2 , entry_list_by_time_2020, bar_width, alpha=0.4, color='red', label='2020')
b2 = plt.bar(index + 0.2  , entry_list_by_time_2021, bar_width, alpha=0.4, color='blue', label='2021')
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
#for num in x_axis :
#    plt.axvline(x = num, color ='r', linestyle='--', linewidth=0.5)
plt.xticks(x_axis, label_x_axis)
plt.xlabel('시간')
plt.ylabel('진입차량수(일반)')
plt.title('2020 & 2021년 실내 체육관 주차장 진입차량수(일반)')
plt.legend()
plt.show()
#%%
# 2020년 시간별 그래프와 2021년 시간별 그래프 같이 그리기 (꺾은선 그래프)
plt.figure(figsize=(15,10))

plt.plot(x_axis, entry_list_by_time_2020, label = '2020', color = 'red', marker = "*")
plt.plot(x_axis, entry_list_by_time_2021, label = '2021', color = 'blue', marker = "*")

plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xlabel('시간')
plt.ylabel('진입차량수(일반)')
plt.title('2020 & 2021년 실내 체육관 주차장 진입차량수(일반)')
plt.legend()
plt.show()
#%%
# 진출차량수
# 2020년 
data_2020 = data[data['연도'] == 2020]

exit_list_by_time_2020 = []
for i in range(24) :
    time = str(i) + ':00 ~ ' + str(i+1) + ':00'
    globals()['exit_data_2020_{}_{}'.format(i,i+1)] =  int(sum(data_2020[data_2020['시간대'] == time].loc[:, '진출차량수(일반)']) / 12)
    exit_list_by_time_2020.append(globals()['exit_data_2020_{}_{}'.format(i,i+1)])
#%%
# 2020년 시간별 그래프 그리기
plt.figure(figsize=(20,15))
x_axis = [i for i in range(24)]
plt.bar(x_axis, exit_list_by_time_2020, color='red')
plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xlabel('시간')
plt.ylabel('진출차량수(일반)')
plt.title('2020년 실내 체육관 주차장 진출차량수(일반)')
plt.show()
#%%
# 2021년 
data_2021 = data[data['연도'] == 2021]

exit_list_by_time_2021 = []
for i in range(24) :
    time = str(i) + ':00 ~ ' + str(i+1) + ':00'
    globals()['exit_data_2021_{}_{}'.format(i,i+1)] =  int(sum(data_2021[data_2021['시간대'] == time].loc[:, '진출차량수(일반)']) / 12)
    exit_list_by_time_2021.append(globals()['exit_data_2021_{}_{}'.format(i,i+1)])
#%%
# 2021년 시간별 그래프 그리기
plt.figure(figsize=(20,15))
x_axis = [i for i in range(24)]
plt.bar(x_axis, exit_list_by_time_2021, color='blue')
plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xlabel('시간')
plt.ylabel('진출차량수(일반)')
plt.title('2021년 실내 체육관 주차장 진출차량수(일반)')
plt.show()   
#%%
# 2020년 시간별 그래프와 2021년 시간별 그래프 같이 그리기
plt.figure(figsize=(20,15))
bar_width = 0.4
index = np.arange(24)
b1 = plt.bar(index - 0.2 , exit_list_by_time_2020, bar_width, alpha=0.4, color='red', label='2020')
b2 = plt.bar(index + 0.2  , exit_list_by_time_2021, bar_width, alpha=0.4, color='blue', label='2021')
plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xlabel('시간')
plt.ylabel('진출차량수(일반)')
plt.title('2020 & 2021년 실내 체육관 주차장 진출차량수(일반)')
plt.legend()
plt.show() 
#%%
# 2020년 시간별 그래프와 2021년 시간별 그래프 같이 그리기 (꺾은선 그래프)
plt.figure(figsize=(15,10))

plt.plot(x_axis, exit_list_by_time_2020, label = '2020', color = 'red', marker = "*")
plt.plot(x_axis, exit_list_by_time_2021, label = '2021', color = 'blue', marker = "*")

plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xlabel('시간')
plt.ylabel('진입차량수(일반)')
plt.title('2020 & 2021년 실내 체육관 주차장 진입차량수(일반)')
plt.legend()
plt.show()
#%%
# 연도별 시간대별 진입차량수 & 진출차량수 그래프 같이 그리기plt.figure(figsize=(8,6))
# 진입은 실선, 진출은 점선
plt.figure(figsize=(20,15))
plt.plot(x_axis, entry_list_by_time_2020, label = '2020_entry', color = 'red', marker = "*")
plt.plot(x_axis, entry_list_by_time_2021, label = '2021_entry', color = 'blue', marker = "*")
plt.plot(x_axis, exit_list_by_time_2020, label = '2020 exit', color = 'red', linestyle = "--", marker = "^")
plt.plot(x_axis, exit_list_by_time_2021, label = '2021 exit', color = 'blue', linestyle = "--", marker = "^")
plt.xticks(x_axis, label_x_axis)
plt.tick_params(axis='x',direction = 'out', length=10, pad=10, labelsize=10, width = 2,  color='r', labelrotation = 30)
plt.xlabel('시간')
plt.ylabel('이동된 차량수')
plt.title('2020 & 2021년 실내 체육관 주차장 진입 & 진출차량수(일반)')
plt.legend()
plt.show() 
#%%
'''
===============================================================================

여기에서 찾은 인사이트는 시간대별로 진입차량이 진출차량보다 많은 구간이 있다.
만약에 이 시간대에 불법 주정차가 발생했다면 좋은 분석 자료가 될 것임
8시~ 13시, 17시~19시

===============================================================================
'''
#%%
# 월별 데이터 분석 

# 2020년
# 진입차량수

data_2020 = data[data['연도'] == 2020]

entry_list_by_month_2020 = []
for i in range(1, 13) :
    globals()['entry_data_2020_{}'.format(i)] =  int(sum(data_2020[data_2020['월'] == i].loc[:, '진입차량수(일반)']))
    entry_list_by_month_2020.append(globals()['entry_data_2020_{}'.format(i)])

# 2020년 월 별 그래프 그리기
plt.figure(figsize=(8,6))
x_axis = [i for i in range(1, 13)]
label_x_axis = [str(i) +'월' for i in range(1, 13)]
plt.bar(x_axis, entry_list_by_month_2020, color='red', width = 0.4)
plt.xticks(x_axis, label_x_axis)
plt.xlabel('월')
plt.ylabel('진입차량수(일반)')
plt.title('2020년 실내 체육관 주차장 진입차량수(일반)')
plt.show() 
#%%

# 2021년
# 진입차량수

data_2021 = data[data['연도'] == 2021]

entry_list_by_month_2021 = []
for i in range(1, 13) :
    globals()['entry_data_2021_{}'.format(i)] =  int(sum(data_2021[data_2021['월'] == i].loc[:, '진입차량수(일반)']))
    entry_list_by_month_2021.append(globals()['entry_data_2021_{}'.format(i)])

# 2020년 월 별 그래프 그리기
plt.figure(figsize=(8,6))
x_axis = [i for i in range(1, 13)]

plt.bar(x_axis, entry_list_by_month_2021, color = 'blue', width = 0.4)
plt.xticks(x_axis, label_x_axis)
plt.xlabel('월')
plt.ylabel('진입차량수(일반)')
plt.title('2021년 실내 체육관 주차장 진입차량수(일반)')
plt.show() 
#%%
# 2020년 월별 그래프와 2021년 월별 그래프 같이 그리기
plt.figure(figsize=(8,6))
plt.plot(x_axis, entry_list_by_month_2020, color ='red', label = '2020', marker='*')
plt.plot(x_axis, entry_list_by_month_2021, color = 'blue', label = '2021', marker = '*')
plt.xticks(x_axis, label_x_axis)
plt.xlabel('월')
plt.ylabel('진입차량수(일반)')
plt.title('2020 & 2021년 실내 체육관 주차장 진입차량수(일반)')
plt.legend()
plt.show()
#%%

# 2020년 
# 진출차량수

data_2020 = data[data['연도'] == 2020]

exit_list_by_month_2020 = []
for i in range(1, 13) :
    globals()['exit_data_2020_{}'.format(i)] =  int(sum(data_2020[data_2020['월'] == i].loc[:, '진출차량수(일반)']))
    exit_list_by_month_2020.append(globals()['exit_data_2020_{}'.format(i)])

# 2020년 월 별 그래프 그리기
plt.figure(figsize=(8,6))
x_axis = [i for i in range(1, 13)]
plt.bar(x_axis, exit_list_by_month_2020, color='red', width = 0.4)
plt.xticks(x_axis, label_x_axis)
plt.xlabel('월')
plt.ylabel('진출차량수(일반)')
plt.title('2020년 실내 체육관 주차장 진출차량수(일반)')
plt.show() 
#%%

# 2021년 
# 진출차량수

data_2021 = data[data['연도'] == 2021]

exit_list_by_month_2021 = []
for i in range(1, 13) :
    globals()['exit_data_2021_{}'.format(i)] =  int(sum(data_2021[data_2021['월'] == i].loc[:, '진출차량수(일반)']))
    exit_list_by_month_2021.append(globals()['exit_data_2021_{}'.format(i)])

# 2021년 월 별 그래프 그리기
plt.figure(figsize=(8,6))
x_axis = [i for i in range(1, 13)]
plt.bar(x_axis, exit_list_by_month_2021, color='blue', width = 0.4)
plt.xticks(x_axis, label_x_axis)
plt.xlabel('월')
plt.ylabel('진출차량수(일반)')
plt.title('2021년 실내 체육관 주차장 진출차량수(일반)')
plt.show() 
#%%
# 2020년 월 별 그래프와 2021년 월별 그래프 같이 그리기
plt.figure(figsize=(8,6))
plt.plot(x_axis, exit_list_by_month_2020, color ='red', label = '2020', marker='*')
plt.plot(x_axis, exit_list_by_month_2021, color = 'blue', label = '2021', marker = '*')
plt.xticks(x_axis, label_x_axis)

plt.xlabel('월')
plt.ylabel('진출차량수(일반)')
plt.title('2020 & 2021년 실내 체육관 주차장 진출차량수(일반)')
plt.legend()
plt.show()
#%%
'''
===============================================================================

(검증 필요) 동일 연도 월 별 진입차량 그래프와 진출 차량 그래프가 상당히 유사
여기에서도 진입량이 많은 월이 존재함
3월부터 11월까지는 진입차량이 진출차량보다 더 많은 구간이고 진입차량이 폭발적으로 늘어나는 시기는 2월~5월까지

===============================================================================
'''