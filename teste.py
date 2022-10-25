segundos = 5130

horas = segundos // 3600
minutos = segundos % 3600 // 60
resto = segundos % 3600 % 60

print(horas, minutos, resto)
