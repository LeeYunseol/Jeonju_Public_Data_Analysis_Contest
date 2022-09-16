import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('C:/Users/hyunj/Desktop/전주공모전자료/제공받은데이터/전라북도 전주시_불법주정차 단속현황_20220830.csv', encoding = 'CP949')

print(data['단속구분'].value_counts())
#%%
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgunbd.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
#%%

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
#font_path = 'C:/Users/hyunj/AppData\Local/Microsoft/Windows/Fonts/NanumGothic.TTF'
font = font_manager.FontProperties(fname=font_path).get_name()
print(font)
rc('font', family=font)

import matplotlib as mpl
#%%
print(mpl.rcParams['font.family'])
print(mpl.rcParams['font.size'])
#%%

#mpl.rcParams['font.family'] = 'NanumGothicExtraBold'
mpl.rcParams['font.size'] = 15

# 전체 1036457
# 고정식CCTV 299435 + 245280 => 52.56%
# 이동식 CCTV 366509 => 35.36%
# 인력단속 35662 + 8612 => 4.27%
# 민원신고 34681 + 32504 => 6.50%
# 기타 13681 + 8612 + 73 + 19 + 1 =>  1.31% 

ratio = [52.56, 35.36, 4.27, 6.50, 1.31]
labels = ['고정식CCTV', '이동식CCTV', '인력단속', '민원신고', '기타']
colors = ['#ff5d46', '#4bc6fe', '#41b8a9', '#dcfbcc', '#f9e0e8']
wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 1}
explode = [0.05, 0.05, 0.05, 0.05, 0.05]

plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=150, counterclock=False, colors=colors, explode = explode, shadow = True, wedgeprops=wedgeprops)
plt.show()
