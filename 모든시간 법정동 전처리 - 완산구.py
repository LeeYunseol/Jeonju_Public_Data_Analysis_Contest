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
완산구 오전 분석
===============================================================================
'''
data_cctv_wansan = data_cctv.loc[(data_cctv['관리'] == '완산')]
data_wansan = data.loc[(data['구청구분'] == '완산구') & (data['단속구분'] == '고정형CCTV단속')]

data_cctv_wansan.reset_index(inplace = True)
data_wansan.reset_index(inplace = True)

missing_wansan = {}

for i in tqdm(range(len(data_wansan)), desc = "완산구 데이터 처리중") :
    place = data_wansan.loc[i, '단속장소명']
    temp_list = place.split()
    find_state = False
    
    for j in range(len(data_cctv_wansan)) :
        establish_place = data_cctv_wansan.loc[j, '설치위치']
        address = data_cctv_wansan.loc[j, '주  소']
        dong = data_cctv_wansan.loc[j, '법정동']
        # new_address = data_cctv_dukjin.loc[i, '신주소']
        
        # 만약 단속장소명을 split한게 법정동과 같다면
        if temp_list[0] == dong :
            data_cctv_wansan.loc[j, '단속수'] += 1
            find_state = True
            break
        
        
        for word in temp_list :
            
            # 만약 단속장소명을 split한게 설치위치와 같다면
            if word in establish_place :
                data_cctv_wansan.loc[j, '단속수'] += 1
                find_state = True
                break
            
            # 만약 단속장소명을 split한게 주소와 같다면
            if word in address :
                data_cctv_wansan.loc[j, '단속수'] += 1
                find_state = True
                break
            
            one_word_state = False
            # 한글자씩 조회해서도 찾았을때도 찾았다고 알려줘야함
            # 이렇게 위에 다 찾아봤는데 안 나왔다면 place변수를 기준으로 한 글짜식 주소에서 찾아보기
            for k in range(4, len(place)) :
                if place[0:k] in establish_place :
                    data_cctv_wansan.loc[j, '단속수'] += 1
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
'''
전체 Missing 값 76539개에서  1000개가 넘는 지역은 일일이 입력
E마트 - 8462   => 서신동
NH전북지사후문 - 1202    => 서노송동
기전대기숙사사거리 - 1309, 기전대기숙사사거리CCTV - 2010   =>  중화산동
대우대창아파트 - 5551, 대우대창인근도로 - 1228    => 서신동
 자성당사거리 - 1711, 복자성당사거리CCTV - 1459   => 다가동4가
삼익아파트삼인당약국 - 1130, 삼천삼익아파트인근CCTV - 1073   => 삼천동1가
서신롯데백화점CCTV - 1881   => 서신동
서신이마트CCTV - 1253, 서신제일비사벌앞CCTV - 1133,   => 서신동
소상공인지원센터CCTV - 2988, 소상공인홍보지원센터 - 2448,   => 전동
어의당한방병원사거리 - 1629, 어의당한방병원인근CCTV - 1085,   => 다가동3가
전주영화제작소 - 1544, 전주영화제작소CCTV - 1687, 정다운약국 - 1181,   => 고사동
풍남관광호텔사거리 - 1395, 풍남관광호텔사거리CCTV - 1043,   => 고사동
풍남문로터리농협 - 4243, 풍남문로터리농협CCTV - 3850, 풍남문로터리편의점 - 1205, 풍남문로터리편의점CCTV - 1590,   => 전동
효자상공회의소후문CCTV - 1398, 효자성우아르데코CCTV - 1030,   => 효자동3가
효자신원아침정문CCTV - 1100, 효자코아루성우후문CCTV - 2312, 효천우미린2차우전교CCTV - 1034   => 효자동3가
'''
#%%
temp_df.loc[temp_df['법정동'] == '서신동', '단속수'] = temp_df.loc[temp_df['법정동'] == '서신동', '단속수'] + 8462 + 1228 + 5551 + 1881 + 1253 + 1133
temp_df.loc[temp_df['법정동'] == '서노송동', '단속수'] = temp_df.loc[temp_df['법정동'] == '서노송동', '단속수'] + 1202
temp_df.loc[temp_df['법정동'] == '중화산동', '단속수'] = temp_df.loc[temp_df['법정동'] == '중화산동', '단속수'] + 1309 + 2010
temp_df.loc[temp_df['법정동'] == '다가동4가', '단속수'] = temp_df.loc[temp_df['법정동'] == '다가동4가', '단속수'] + 1711 + 1459 
temp_df.loc[temp_df['법정동'] == '삼천동1가', '단속수'] = temp_df.loc[temp_df['법정동'] == '삼천동1가', '단속수'] + 1130 + 1073 
temp_df.loc[temp_df['법정동'] == '전동', '단속수'] = temp_df.loc[temp_df['법정동'] == '전동', '단속수'] + 2988 + 2448 + 4243 + 3850 + 1205 + 1590
temp_df.loc[temp_df['법정동'] == '다가동3가', '단속수'] = temp_df.loc[temp_df['법정동'] == '다가동3가', '단속수'] +1629 + 1085
temp_df.loc[temp_df['법정동'] == '고사동', '단속수'] = temp_df.loc[temp_df['법정동'] == '고사동', '단속수'] + 1544 + 1687 + 1181 + 1395 + 1043
temp_df.loc[temp_df['법정동'] == '효자동3가', '단속수'] = temp_df.loc[temp_df['법정동'] == '효자동3가', '단속수'] +1398 + 1030 + 1100 + 2312 + 1034
#%%
# 데이터프레임으로 저장
temp_df.to_csv('모든시간 완산구 고정식CCTV 단속현황.csv', index = False, encoding = 'CP949')
