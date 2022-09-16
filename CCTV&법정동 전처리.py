# 두 개의 csv를 통합해서 법정동 별로 불법 주정차 현황을 시각화

# 라이브러리 임포트
import pandas as pd
from tqdm import tqdm
#%%
data_cctv = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차단속카메라현황.csv')
# 불법 주정차 현황
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전처리된 불법주정차현황.csv', encoding = 'CP949')
#%%
'''
# 단속현황에 '인후동xxx'로 띄어쓰기 하지 않고 나타나 있기 때문에 동을 기준으로 무조건 띄어쓰기로 바꿔주기
for i in tqdm(range(len(data)), desc = "동을 동 으로 바꾸는 중") :
    data.loc[i, '단속장소명'] = data.loc[i, '단속장소명'].replace('동', '동 ')
    data.loc[i, '단속장소명'] = data.loc[i, '단속장소명'].replace('(', ' (')
'''
#%%
'''
===============================================================================
덕진구 오전 먼저 분리해서 보기
===============================================================================
'''
data_cctv_dukjin = data_cctv.loc[(data_cctv['관리'] == '덕진')]
data_dukjin = data.loc[(data['구청구분'] == '덕진구') & (data['단속구분'] == '고정식CCTV') & (data['단속된 시간'] == 10)] 

data_cctv_dukjin.reset_index(inplace = True)
data_dukjin.reset_index(inplace = True)

missing_dukjin = {}

for i in tqdm(range(len(data_dukjin)), desc = "덕진구 데이터 처리중") :
    place = data_dukjin.loc[i, '단속장소명']
    temp_list = place.split()
    find_state = False
    
    for j in range(len(data_cctv_dukjin)) :
        establish_place = data_cctv_dukjin.loc[j, '설치위치']
        address = data_cctv_dukjin.loc[j, '주  소']
        dong = data_cctv_dukjin.loc[j, '법정동']
        # new_address = data_cctv_dukjin.loc[i, '신주소']
        
        # 만약 단속장소명을 split한게 법정동과 같다면
        if temp_list[0] == dong :
            data_cctv_dukjin.loc[j, '단속수'] += 1
            find_state = True
            break
        
        
        for word in temp_list :
            
            # 만약 단속장소명을 split한게 설치위치와 같다면
            if word in establish_place :
                data_cctv_dukjin.loc[j, '단속수'] += 1
                find_state = True
                break
            
            # 만약 단속장소명을 split한게 주소와 같다면
            if word in address :
                data_cctv_dukjin.loc[j, '단속수'] += 1
                find_state = True
                break
            
            one_word_state = False
            # 한글자씩 조회해서도 찾았을때도 찾았다고 알려줘야함
            # 이렇게 위에 다 찾아봤는데 안 나왔다면 place변수를 기준으로 한 글짜식 주소에서 찾아보기
            for k in range(3, len(place)) :
                if place[0:k] in establish_place :
                    data_cctv_dukjin.loc[j, '단속수'] += 1
                    find_state = True
                    one_word_state = True
                    break
            if one_word_state == True :
                break
            
        if find_state == True :
            # 이미 찾았으니 cctv 안에서 돌면서 찾는 것도 break로 멈춤
            break
            
     # 만약에 못 찾았다?
    if find_state == False :
        if place not in missing_dukjin :
            missing_dukjin[place] = 1
        else :
            missing_dukjin[place] += 1 
    
#%%
# cctv 단속에 들어간 수보다 덕진구에서 발생한 불법주정차 수보다 낮은지 확인
print('들어간 cctv 단속수 개수 : ', sum(data_cctv_dukjin['단속수']))
# missing value 값들 확인
print('MISSING 값들 확인 : ', sum(missing_dukjin.values()) )
#%%
temp_df = data_cctv_dukjin.groupby(['법정동'])['단속수'].sum().reset_index()
'''
Missing 값에서 100건 이상의 값을 채택
농협아중지점 - 379, 만성에코르아파트후문 - 261, 송천1동 솔내고앞 - 350, 송천1동 오송중앞 - 131,
# 에코스위첸 (듬뿍마트앞) - 1506, 여의영무예다움상가주변 - 1254
들은 중요하다고 판단되어 따로 위치를 검색한 후에 더해줌

농협아중지점 => 인후동1가
만성에코르아파트후문 => 만성동
송천1동 솔내고앞 => 송천동1가
송천1동 오송중앞 => 송천동1가

에코스위첸 => 송천동2가
여의영무예다움상가주변 => 여의동 2가
'''
#%%
temp_df.loc[temp_df['법정동'] == '인후동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '인후동1가', '단속수'] + 379
temp_df.loc[temp_df['법정동'] == '만성동', '단속수'] = temp_df.loc[temp_df['법정동'] == '만성동', '단속수'] + 261
temp_df.loc[temp_df['법정동'] == '송천동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '송천동1가', '단속수'] + 481

#%%
# 데이터프레임으로 저장
temp_df.to_csv('전처리된 덕진구 오전 불법주정차현황.csv', index = False, encoding = 'CP949')

#%%
data_cctv = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차단속카메라현황.csv')
data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전처리된 불법주정차현황.csv', encoding = 'CP949')

'''
===============================================================================
덕진구 오후(14시~17시) 분리해서 보기
===============================================================================
'''
data_cctv_dukjin = data_cctv.loc[(data_cctv['관리'] == '덕진')]
data_dukjin = data.loc[(data['구청구분'] == '덕진구') & (data['단속구분'] == '고정식CCTV')] 
data_dukjin = data_dukjin.loc[(data_dukjin['단속된 시간'] == 14) | (data_dukjin['단속된 시간'] == 15) | (data_dukjin['단속된 시간'] == 16)]

data_cctv_dukjin.reset_index(inplace = True)
data_dukjin.reset_index(inplace = True)

missing_dukjin = {}

for i in tqdm(range(len(data_dukjin)), desc = "덕진구 데이터 처리중") :
    place = data_dukjin.loc[i, '단속장소명']
    temp_list = place.split()
    find_state = False
    
    for j in range(len(data_cctv_dukjin)) :
        establish_place = data_cctv_dukjin.loc[j, '설치위치']
        address = data_cctv_dukjin.loc[j, '주  소']
        dong = data_cctv_dukjin.loc[j, '법정동']
        # new_address = data_cctv_dukjin.loc[i, '신주소']
        
        # 만약 단속장소명을 split한게 법정동과 같다면
        if temp_list[0] == dong :
            data_cctv_dukjin.loc[j, '단속수'] += 1
            find_state = True
            break
        
        
        for word in temp_list :
            
            # 만약 단속장소명을 split한게 설치위치와 같다면
            if word in establish_place :
                data_cctv_dukjin.loc[j, '단속수'] += 1
                find_state = True
                break
            
            # 만약 단속장소명을 split한게 주소와 같다면
            if word in address :
                data_cctv_dukjin.loc[j, '단속수'] += 1
                find_state = True
                break
            
            one_word_state = False
            # 한글자씩 조회해서도 찾았을때도 찾았다고 알려줘야함
            # 이렇게 위에 다 찾아봤는데 안 나왔다면 place변수를 기준으로 한 글짜식 주소에서 찾아보기
            for k in range(3, len(place)) :
                if place[0:k] in establish_place :
                    data_cctv_dukjin.loc[j, '단속수'] += 1
                    find_state = True
                    one_word_state = True
                    break
            if one_word_state == True :
                break
            
        if find_state == True :
            # 이미 찾았으니 cctv 안에서 돌면서 찾는 것도 break로 멈춤
            break
            
     # 만약에 못 찾았다?
    if find_state == False :
        if place not in missing_dukjin :
            missing_dukjin[place] = 1
        else :
            missing_dukjin[place] += 1 
    
#%%
# cctv 단속에 들어간 수보다 덕진구에서 발생한 불법주정차 수보다 낮은지 확인
print('들어간 cctv 단속수 개수 : ', sum(data_cctv_dukjin['단속수']))
# missing value 값들 확인
print('MISSING 값들 확인 : ', sum(missing_dukjin.values()) )
#%%
temp_df = data_cctv_dukjin.groupby(['법정동'])['단속수'].sum().reset_index()
'''
Missing 값에서 1000건에 가까운 값을 채택
농협아중지점 - 1461, 만성에코르아파트후문 - 1163, 송천1동 솔내고앞 - 1055, 송천1동 오송중앞 - 953,
# 에코스위첸 (듬뿍마트앞) - 1506, 여의영무예다움상가주변 - 1254
들은 중요하다고 판단되어 따로 위치를 검색한 후에 더해줌

농협아중지점 => 인후동1가
만성에코르아파트후문 => 만성동
송천1동 솔내고앞 => 송천동1가
송천1동 오송중앞 => 송천동1가

에코스위첸 => 송천동2가
여의영무예다움상가주변 => 여의동 2가
'''
temp_df.loc[temp_df['법정동'] == '인후동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '인후동1가', '단속수'] + 1461
temp_df.loc[temp_df['법정동'] == '만성동', '단속수'] = temp_df.loc[temp_df['법정동'] == '만성동', '단속수'] + 1163
temp_df.loc[temp_df['법정동'] == '송천동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '송천동1가', '단속수'] + 2008

#%%
# 데이터프레임으로 저장
temp_df.to_csv('전처리된 덕진구 오후 불법주정차현황.csv', index = False, encoding = 'CP949')
