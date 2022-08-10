import requests
import pprint


#인증키 입력
encoding = 'WuXM62rU69nEO665oRKxgjH6yq8GZgre2u2MuLxL5JnYtwe65RdDvc1n4kvg6HcH9YrG1nRpEC5L1rrZ9SkqLg%3D%3D'
decoding = 'WuXM62rU69nEO665oRKxgjH6yq8GZgre2u2MuLxL5JnYtwe65RdDvc1n4kvg6HcH9YrG1nRpEC5L1rrZ9SkqLg=='

#url 입력
url = 'http://openapi.jeonju.go.kr/rest/parking'
params ={'serviceKey' : encoding , 'pageNo' : '1', 'numOfRows' : '10', 'startCreateDt' : '2020', 'endCreateDt' : '20211103' }

response = requests.get(url, params=params)

# xml 내용
content = response.text

# 깔끔한 출력 위한 코드
pp = pprint.PrettyPrinter(indent=4)
#print(pp.pprint(content))

### xml을 DataFrame으로 변환하기 ###
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote

## 각 컬럼 값 ## (포털 문서에서 꼭 확인하세요)
"""
SEQ : 게시글번호(국내 시도별 발생현황 고유값)
CREATE_DT: 	등록일시분초
DEATH_CNT: 	사망자 수
GUBUN: 	시도명(한글)
GUBUN_CN: 	시도명(중국어)
gubunEn: 시도명(영어)
INC_DEC: 전일대비 증감 수
ISOL_CLEAR_CNT: 격리 해제 수
QUR_RATE: 10만명당 발생률
STD_DAY: 기준일시
UPDATE_DT: 수정일시분초
DEF_CNT: 확진자 수
ISOL_ING_CNT: 격리중 환자수
OVER_FLOW_CNT: 해외유입 수
LOCAL_OCC_CNT: 지역발생 수

""" 

#bs4 사용하여 item 태그 분리

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('item')
print(rows)
"""
# 컬럼 값 조회용
columns = rows[0].find_all()
print(columns)
"""

# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]

#xml값 DataFrame으로 만들기
corona_df = pd.DataFrame(row_list, columns=name_list)
print(corona_df.head(19)) 

#DataFrame CSV 파일로 저장
corona_df.to_csv('corona_kr.csv', encoding='utf-8-sig')