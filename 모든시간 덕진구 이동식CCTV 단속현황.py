# 두 개의 csv를 통합해서 법정동 별로 불법 주정차 현황을 시각화

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
모든 시간  보기
===============================================================================
'''

data_cctv_dukjin = data_cctv.loc[(data_cctv['관리'] == '덕진')]
data_dukjin = data.loc[(data['구청구분'] == '덕진구') & (data['단속구분'] == '이동식CCTV')] 

data_cctv_dukjin.reset_index(inplace = True)
data_dukjin.reset_index(inplace = True)

missing_dukjin = {}

for i in tqdm(range(len(data_dukjin)), desc = "덕진구 데이터 처리중") :
    place = data_dukjin.loc[i, '단속장소명']
    temp_list = place.split()
    find_state = False
    
    for j in range(len(data_cctv_dukjin)) :
        road_name = data_cctv_dukjin.loc[j, '도로명']
        dong = data_cctv_dukjin.loc[j, '법정동']
        # new_address = data_cctv_dukjin.loc[i, '신주소']
        
        # 단속장소명이 한 글자인경우가 있음, '덕진동2가' 이렇게 되ㅐ어 있으면 쉽게 가능한데, 편운로 or 전북대병원입구 or 만성.. 이면 귀찮아짐
        # 한글자가 만약에 법정동이라면 조회하고 끝내야 함. 그래야 밑에서 안 걸림
        if (len(temp_list) == 1) and (temp_list[0] == dong) :
                data_cctv_dukjin.loc[j, '단속수'] += 1
                find_state = True
                break
        
        # 그냥 못 찾은거니 missing 딕셔너리에서 확인해보자
        if (len(temp_list) == 1) and (temp_list[0] != dong) :
            break
            
        # 만약 단속장소명을 split한게 법정동과 같다면
        if temp_list[0] == dong :
            data_cctv_dukjin.loc[j, '단속수'] += 1
            find_state = True
            break
        
        if (temp_list[0] in dong) and (temp_list[1] == road_name):
            data_cctv_dukjin.loc[j, '단속수'] += 1
            find_state = True
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
[ 100에 가까운 값을 선택 ]
전체 325211 개의 MISSING 값


기지로 : 1130 => 중동인지 만성동인지 모른다 제외
덕진동 가련산로 : 2503 => 덕진동2가
덕진동 가리내로 : 480 => 숫자에 따라 덕진동1가가 될 수 있고 2가가 될 수 있음 => 제외
덕진동 들사평2길 : 121 => 덕진동1가
덕진동 들사평3길 : 135 => 덕진동1가
덕진동 명륜5길 : 184 => 덕진동1가
덕진동 추탄로 : 438 => 덕진동2가
동산동 쪽구름~~ 다 여의동이래 : 2+21+3+93+13+46+44+12+730+6+2200 => 여의동
산정동 : 4165     => 산정동

140 => 서노송동

송천동 가리내로 : 210 => 송천동1가
송천동 두간로 : 465 => 송천동1가
송천동 붓내3길 : 1043 => 송천동2가
송천동 사근1길 : 392 => 숫자에 따라서 달라질 수 있음 제외
송천동 1가 -> 18+160+24+608+626+71+119+2543+205+1159+319+70+42+47
안전로 486 -> 중동인지 장동인지 모름
오공로 : 893 => 중동인지 만성동인지 모름
우아동 도당산1길 : 830 => 우아동 3가

우아동 아중로 157 => 우아동3가
우아동 안덕원로 & 안덕원1길 : 911 + 220  => 우아동3가

우아동 정언신로 : 616 -> 우아동2가
우아동 중상보로 : 614=> 우아동2가
우아동 호성1길 : 711 => 우아동3가
인후동 아중로 : 943 => 인후동1가
인후동 정언신로 : 743 => 인후동1가
인후동 한배미로 : 595 => 인후동1가
호성동1가 655+1042
'''

#%%
temp_df.loc[temp_df['법정동'] == '인후동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '인후동1가', '단속수'] + 943 + 743 + 595
temp_df.loc[temp_df['법정동'] == '덕진동2가', '단속수'] = temp_df.loc[temp_df['법정동'] == '덕진동2가', '단속수'] + 2503 + 438 
temp_df.loc[temp_df['법정동'] == '덕진동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '덕진동1가', '단속수'] + 121 + 135 + 184 
temp_df.loc[temp_df['법정동'] == '여의동', '단속수'] = temp_df.loc[temp_df['법정동'] == '여의동', '단속수'] + 2+21+3+93+13+46+44+12+730+6+2200 
temp_df.loc[temp_df['법정동'] == '산정동', '단속수'] = temp_df.loc[temp_df['법정동'] == '산정동', '단속수'] + 4165
temp_df.loc[temp_df['법정동'] == '서노송동', '단속수'] = temp_df.loc[temp_df['법정동'] == '서노송동', '단속수'] + 140
temp_df.loc[temp_df['법정동'] == '송천동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '송천동1가', '단속수'] + 210 + 465 + 18+160+24+608+626+71+119+2543+205+1159+319+70+42+47
temp_df.loc[temp_df['법정동'] == '송천동2가', '단속수'] = temp_df.loc[temp_df['법정동'] == '송천동2가', '단속수'] + 1043
temp_df.loc[temp_df['법정동'] == '우아동3가', '단속수'] = temp_df.loc[temp_df['법정동'] == '우아동3가', '단속수'] + 830 + 157 + 911 + 220 + 711
temp_df.loc[temp_df['법정동'] == '우아동2가', '단속수'] = temp_df.loc[temp_df['법정동'] == '우아동2가', '단속수'] + 616 + 614
temp_df.loc[temp_df['법정동'] == '호성동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '호성동1가', '단속수'] + 655 + 1042

#%%
# 데이터프레임으로 저장
temp_df.to_csv('모든시간 덕진구 이동식CCTV 단속현황.csv', index = False, encoding = 'CP949')