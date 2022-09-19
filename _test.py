import datetime

data_atual = datetime.datetime.now()
data_atual = "2022-09-18/13:11:40.630347"
data_atual = datetime.datetime.strptime(data_atual, "%y-%m-%d/%H:%M:%f")

print(data_atual)