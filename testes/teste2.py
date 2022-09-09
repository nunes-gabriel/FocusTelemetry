import pandas as pd

df = pd.read_csv(r"\\Server\python-matutino\gabriel.nunes\Documents\GitHub\TCC-GestaoLogistica\testes\cidades.csv")
df = df.drop(columns=["id_municipio"])

df.to_csv(r"\\Server\python-matutino\gabriel.nunes\Documents\GitHub\TCC-GestaoLogistica\testes\cidades2.csv", sep=",")