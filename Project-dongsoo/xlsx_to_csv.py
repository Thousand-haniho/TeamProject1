import pandas as pd

xlsx = pd.read_excel("./resData/농작물사전.xlsx")
xlsx.to_csv("./resData/농작물사전.csv")