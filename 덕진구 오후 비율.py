"""
덕진구 오전 이동식 / 고정식 비율 구하기
"""

# 라이브러리 임포트
import pandas as pd
from tqdm import tqdm
#%%
data_cctv = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차단속카메라현황2.csv')
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
    if data.loc[i, "단속장소명"] == "덕진동덕암마을" :
        data.loc[i, "단속장소명"] = "덕암마을"
        
    if data.loc[i, "단속장소명"] == "만성에코르아파트후문" :
        data.loc[i, "단속장소명"] = "에코르아파트"
    
    if data.loc[i, "단속장소명"] == "반월동주공아파트앞" :
        data.loc[i, "단속장소명"] = "반월주공아파트"
        
    if data.loc[i, "단속장소명"] == "송천1동오송중앞" :
        data.loc[i, "단속장소명"] = "오송중학교"
        
    if data.loc[i, "단속장소명"] == "팔복동근린상가" :
        data.loc[i, "단속장소명"] = "팔복동 근린상가"
        
    if data.loc[i, "단속장소명"] == "인후동휴플러스아파트" :
        data.loc[i, "단속장소명"] = "휴플러스"
        
    if data.loc[i, "단속장소명"] == "인후동휴프러스아파트" :
        data.loc[i, "단속장소명"] = "휴플러스 "
    
    if data.loc[i, "단속장소명"] == "모래내북측(이남심내과)" :
        data.loc[i, "단속장소명"] = "이남심내과 "
        
    if data.loc[i, "단속장소명"] == "금암동휴엔하임아파트주" :
        data.loc[i, "단속장소명"] = "금암휴엔하임 "
        
    if data.loc[i, "단속장소명"] == "인후동에버파크" :
        data.loc[i, "단속장소명"] = "에버파크"
        
    if data.loc[i, "단속장소명"] == "검찰청입구" :
        data.loc[i, "단속장소명"] = "검찰청"
    
    if data.loc[i, "단속장소명"] == "에코시티 데시앙7차 주변" :
        data.loc[i, "단속장소명"] = "7단지"
    
    if data.loc[i, "단속장소명"] == "에코시티 데시앙5차 주변" :
        data.loc[i, "단속장소명"] = "5단지"
    
    if data.loc[i, "단속장소명"] == "에코시티 데시앙12블럭" :
        data.loc[i, "단속장소명"] = "12단지"

    if data.loc[i, "단속장소명"] == "에에코시티 자이103동 앞" :
        data.loc[i, "단속장소명"] = "자이1차"
        
    if data.loc[i, "단속장소명"] == "농협아중지점" :
        data.loc[i, "단속장소명"] = "아중새천년약국"
    
    if data.loc[i, "단속장소명"] == "e편한세상아파트 정문" :
        data.loc[i, "단속장소명"] = "이편한세상"
        
    if data.loc[i, "단속장소명"] == "파인트리몰 정문" :
        data.loc[i, "단속장소명"] = "파인트리몰정문"

    if data.loc[i, "단속장소명"] == "파인트리몰 후문" :
        data.loc[i, "단속장소명"] = "파인트리몰후문"

    if data.loc[i, "단속장소명"] == "만성동 양현초 근처" :
        data.loc[i, "단속장소명"] = "양현초"
        
    if data.loc[i, "단속장소명"] == "송천동 솔내동아사거리" :
        data.loc[i, "단속장소명"] = "솔내동아"
#%%
"""
덕진구 오전 ★고정식★ 먼저 
"""
data_cctv_dukjin = data_cctv.loc[(data_cctv['관리'] == '덕진')]
data_dukjin = data.loc[(data['구청구분'] == '덕진구') & (data['단속구분'] == '고정식CCTV')] 
data_dukjin = data_dukjin.loc[(data_dukjin['단속된 시간'] == 14) | (data_dukjin['단속된 시간'] == 15) | (data_dukjin['단속된 시간'] == 16) | (data_dukjin['단속된 시간'] == 17)]
data_dukjin = data_dukjin.loc[(data_dukjin['년'] == 2018) | (data_dukjin['년'] == 2019) | (data_dukjin['년'] == 2020) | (data_dukjin['년'] == 2021)]

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
        
        for word in temp_list :
            
            # 만약 단속장소명을 split한게 설치위치와 같다면
            if word in establish_place :
                data_cctv_dukjin.loc[j, '고정식_단속수'] += 1
                find_state = True
                break
            
            # 만약 단속장소명을 split한게 주소와 같다면
            if word in address :
                data_cctv_dukjin.loc[j, '고정식_단속수'] += 1
                find_state = True
                break
            
            one_word_state = False
            # 한글자씩 조회해서도 찾았을때도 찾았다고 알려줘야함
            # 이렇게 위에 다 찾아봤는데 안 나왔다면 place변수를 기준으로 한 글짜식 주소에서 찾아보기
            
            for k in range(4, len(place)) :
                if place[0:k] in establish_place :
                    data_cctv_dukjin.loc[j, '고정식_단속수'] += 1
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
print("\n===== 고정식 =====")
print('들어간 cctv 단속수 개수 : ', sum(data_cctv_dukjin['고정식_단속수']))
# missing value 값들 확인
print('MISSING 값들 확인 : ', sum(missing_dukjin.values()) )
#%%
# 데이터 그룹
temp_fix_df = data_cctv_dukjin.groupby(["도로명", "법정동"])["고정식_단속수"].sum()
#%%
"""
덕진구 오전 ★이동식★ 

이거 생각잘해야함

기린대로는 여의동에도 있고 팔복동2가에도 있음
기지로도 만성동에 하나 중동에 하나 있어서 이거 구별 못함
"""
data_cctv_dukjin = data_cctv.loc[(data_cctv['관리'] == '덕진')]
data_dukjin = data.loc[(data['구청구분'] == '덕진구') & (data['단속구분'] == '이동식CCTV')] 
data_dukjin = data_dukjin.loc[(data_dukjin['단속된 시간'] == 14) | (data_dukjin['단속된 시간'] == 15) | (data_dukjin['단속된 시간'] == 16) | (data_dukjin['단속된 시간'] == 17)]
data_dukjin = data_dukjin.loc[(data_dukjin['년'] == 2018) | (data_dukjin['년'] == 2019) | (data_dukjin['년'] == 2020) | (data_dukjin['년'] == 2021)]

data_cctv_dukjin.reset_index(inplace = True)
data_dukjin.reset_index(inplace = True)

missing_dukjin = {}

for i in tqdm(range(len(data_dukjin)), desc = "덕진구 데이터 처리중") :
    place = data_dukjin.loc[i, '단속장소명']
    temp_list = place.split()
    place_dong = temp_list[0]
    find_state = False
    
    for j in range(len(data_cctv_dukjin)) :
        road_name = data_cctv_dukjin.loc[j, '도로명']
        dong = data_cctv_dukjin.loc[j, "법정동"]
        
        
        if len(temp_list) == 1:
            if temp_list[0] != road_name :
                break
            if temp_list[0] == road_name : 
                data_cctv_dukjin.loc[j, '이동식_단속수'] += 1
                find_state = True
                break
                
        if place_dong == dong and road_name == temp_list[1] :
            data_cctv_dukjin.loc[j, '이동식_단속수'] += 1
            find_state = True
            break
        '''
        road_name = data_cctv_dukjin.loc[j, '도로명']
        # dong = data_cctv_dukjin.loc[j, '법정동']
        # new_address = data_cctv_dukjin.loc[i, '신주소']
        
        # 단속장소명이 한 글자인경우가 있음, '덕진동2가' 이렇게 되ㅐ어 있으면 쉽게 가능한데, 편운로 or 전북대병원입구 or 만성.. 이면 귀찮아짐
        # 한글자가 만약에 법정동이라면 조회하고 끝내야 함. 그래야 밑에서 안 걸림
        if (len(temp_list) == 1) and (temp_list[0] == road_name) :
                data_cctv_dukjin.loc[j, '이동식_단속수'] += 1
                find_state = True
                break
            
        # 나중에 확인해보
        if (len(temp_list) == 1) and (temp_list[0] != road_name) :
            break
            
        # 만약 단속장소명을 split한게 법정동과 같다면
        if temp_list[1] == road_name :
            data_cctv_dukjin.loc[j, '이동식_단속수'] += 1
            find_state = True
            break
        '''
     # 만약에 못 찾았다?
    if find_state == False :
        if place not in missing_dukjin :
            missing_dukjin[place] = 1
        else :
            missing_dukjin[place] += 1#%%
print("\n===== 이동식 =====")
print('들어간 cctv 단속수 개수 : ', sum(data_cctv_dukjin['이동식_단속수']))
# missing value 값들 확인
print('MISSING 값들 확인 : ', sum(missing_dukjin.values()) )
#%%

temp = data_dukjin['단속장소명'].value_counts()
temp.to_csv('덕진구 오후 이동식 단속수.csv', encoding = 'CP949')

# 데이터 그룹
temp_move_df = data_cctv_dukjin.groupby(["도로명", "법정동"])["이동식_단속수"].sum()

#%%
# Conacat 
concat_df = pd.concat([temp_fix_df,temp_move_df], axis=1)
#%%
for index in concat_df.index :
    try :            
        num1 = concat_df.loc[index, "이동식_단속수"]
        num2 = concat_df.loc[index, "고정식_단속수"]
        concat_df.loc[index, "비율"] =  num1 / num2 * 100
    except :
        concat_df.loc[index, "비율"] = 0
#%%
concat_df.to_csv('덕진구 오후 비율.csv', encoding = 'CP949')