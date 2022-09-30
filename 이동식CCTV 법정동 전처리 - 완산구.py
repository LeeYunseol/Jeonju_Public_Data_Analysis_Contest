# 라이브러리 임포트
import pandas as pd
from tqdm import tqdm
#%%
data_cctv = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차단속카메라현황.csv')
# 불법 주정차 현황
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차 단속현황_20220830.csv', encoding = 'CP949')
#%%

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
오전 먼저 분리해서 보기

★기린대로는 법정동별로 이름이 같기 때문에 이를 기준으로 조회해서는 안된다★
===============================================================================
'''

data_cctv_wansan = data_cctv.loc[(data_cctv['관리'] == '완산')]
data_wansan = data.loc[(data['구청구분'] == '완산구') & (data['단속구분'] == '이동식CCTV') & (data['단속된 시간'] == 10)] 

data_cctv_wansan.reset_index(inplace = True)
data_wansan.reset_index(inplace = True)

missing_wansan = {}

for i in tqdm(range(len(data_wansan)), desc = "완산구 데이터 처리중") :
    place = data_wansan.loc[i, '단속장소명']
    temp_list = place.split()
    find_state = False
    
    for j in range(len(data_cctv_wansan)) :
        road_name = data_cctv_wansan.loc[j, '도로명']
        dong = data_cctv_wansan.loc[j, '법정동']
        # new_address = data_cctv_dukjin.loc[i, '신주소']
        
        # 단속장소명이 한 글자인경우가 있음, '덕진동2가' 이렇게 되ㅐ어 있으면 쉽게 가능한데, 편운로 or 전북대병원입구 or 만성.. 이면 귀찮아짐
        # 한글자가 만약에 법정동이라면 조회하고 끝내야 함. 그래야 밑에서 안 걸림
        if (len(temp_list) == 1) and (temp_list[0] == dong) :
                data_cctv_wansan.loc[j, '단속수'] += 1
                find_state = True
                break
        
        # 그냥 못 찾은거니 missing 딕셔너리에서 확인해보자
        if (len(temp_list) == 1) and (temp_list[0] != dong) :
            break
            
        # 만약 단속장소명을 split한게 법정동과 같다면
        if temp_list[0] == dong :
            data_cctv_wansan.loc[j, '단속수'] += 1
            find_state = True
            break
        
        if (temp_list[0] in dong) and (temp_list[1] == road_name):
            data_cctv_wansan.loc[j, '단속수'] += 1
            find_state = True
            break
        
     # 만약에 못 찾았다?
    if find_state == False :
        if place not in missing_wansan :
            missing_wansan[place] = 1
        else :
            missing_wansan[place] += 1 
#%%
# cctv 단속에 들어간 수보다 덕진구에서 발생한 불법주정차 수보다 낮은지 확인
print('들어간 cctv 단속수 개수 : ', sum(data_cctv_wansan['단속수']))
# missing value 값들 확인
print('MISSING 값들 확인 : ', sum(missing_wansan.values()) )

# 신기하게 57559 데이터중에서 missing 값은 364개
#%%
temp_df = data_cctv_wansan.groupby(['법정동'])['단속수'].sum().reset_index()

# 데이터프레임으로 저장
temp_df.to_csv('전처리된 완산구 오전 이동식CCTV단속현황.csv', index = False, encoding = 'CP949')

#%%
#%%
data_cctv = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차단속카메라현황.csv')
# data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차 단속현황_20220830.csv', encoding = 'CP949')

'''
===============================================================================
완산구 오후(14시~17시) 분리해서 보기
===============================================================================
'''
data_cctv_wansan = data_cctv.loc[(data_cctv['관리'] == '완산')]
data_wansan = data.loc[(data['구청구분'] == '완산구') & (data['단속구분'] == '이동식CCTV')] 
data_wansan = data_wansan.loc[(data_wansan['단속된 시간'] == 14) | (data_wansan['단속된 시간'] == 15) | (data_wansan['단속된 시간'] == 16) | (data_wansan['단속된 시간'] == 17)]

data_cctv_wansan.reset_index(inplace = True)
data_wansan.reset_index(inplace = True)

missing_wansan = {}

for i in tqdm(range(len(data_wansan)), desc = "완산구 데이터 처리중") :
    place = data_wansan.loc[i, '단속장소명']
    temp_list = place.split()
    find_state = False
    
    for j in range(len(data_cctv_wansan)) :
        road_name = data_cctv_wansan.loc[j, '도로명']
        dong = data_cctv_wansan.loc[j, '법정동']
        # new_address = data_cctv_dukjin.loc[i, '신주소']
        
        # 단속장소명이 한 글자인경우가 있음, '덕진동2가' 이렇게 되ㅐ어 있으면 쉽게 가능한데, 편운로 or 전북대병원입구 or 만성.. 이면 귀찮아짐
        # 한글자가 만약에 법정동이라면 조회하고 끝내야 함. 그래야 밑에서 안 걸림
        if (len(temp_list) == 1) and (temp_list[0] == dong) :
                data_cctv_wansan.loc[j, '단속수'] += 1
                find_state = True
                break
        
        # 그냥 못 찾은거니 missing 딕셔너리에서 확인해보자
        if (len(temp_list) == 1) and (temp_list[0] != dong) :
            break
            
        # 만약 단속장소명을 split한게 법정동과 같다면
        if temp_list[0] == dong :
            data_cctv_wansan.loc[j, '단속수'] += 1
            find_state = True
            break
        
        if (temp_list[0] in dong) and (temp_list[1] == road_name):
            data_cctv_wansan.loc[j, '단속수'] += 1
            find_state = True
            break
        
     # 만약에 못 찾았다?
    if find_state == False :
        if place not in missing_wansan :
            missing_wansan[place] = 1
        else :
            missing_wansan[place] += 1 
    
#%%
# cctv 단속에 들어간 수보다 덕진구에서 발생한 불법주정차 수보다 낮은지 확인
print('들어간 cctv 단속수 개수 : ', sum(data_cctv_wansan['단속수']))
# missing value 값들 확인
print('MISSING 값들 확인 : ', sum(missing_wansan.values()) )
#%%
temp_df = data_cctv_wansan.groupby(['법정동'])['단속수'].sum().reset_index()

# 데이터프레임으로 저장
temp_df.to_csv('전처리된 완산구 오후 이동식CCTV단속현황.csv', index = False, encoding = 'CP949')