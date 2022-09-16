import pandas

dados = pandas.read_csv("./database/_dataframe.csv", delimiter=";")
for linha in dados.iterrows():
    print(dict(linha[1]))
