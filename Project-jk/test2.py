import pandas as pd
from matplotlib import font_manager, rc


font_path = "resData/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

df = pd.read_excel('../resData/가격정보.xlsx', engine='openpyxl', header=1)
df = df.ffill()
mask = (df['등급']=='상품')
df = df[mask]
df = df.drop(df.columns[6:], axis=1)
df = df.drop('등급', axis=1)
df.rename({df.columns[3]: '당일'}, axis=1, inplace=True)
df.rename({df.columns[4]: '1일전'}, axis=1, inplace=True)
df['당일'] = df['당일'].str.replace(',', '').astype(int)
df['1일전'] = df['1일전'].str.replace(',', '').astype(int)
df['품목'] = df['품목'] + '(' + df['단위'] + ')'
df = df.drop('단위', axis=1)
df_grouped = df.groupby('품목', as_index=False).mean(numeric_only=True)
cols = ['당일', '1일전']
df_grouped[cols] = df_grouped[cols].round(0).astype(int)

df_grouped["등락률(%)"] = (
        ((df_grouped["당일"] - df_grouped["1일전"]) / df_grouped["1일전"]) * 100)
df_grouped["등락률(%)"] = df_grouped["등락률(%)"].round(1)

print(df_grouped)
