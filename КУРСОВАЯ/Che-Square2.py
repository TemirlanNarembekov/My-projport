import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from decimal import Decimal
from datetime import datetime
# Задайте путь к CSV файлу
file_path = 'C:\\Users\\user\\Desktop\\КУРСОВАЯ\\may2019-april2024.csv'
epsilon = 1e-10  # Маленькое значение погрешности
# Создаем пустой список для хранения цен и дат
prices = []

# Открываем CSV файл и считываем данные
try:
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if row[1]:  # Проверяем, есть ли данные о цене
                date = datetime.strptime(row[0], '%d.%m.%Y')  # Преобразуем дату в формат datetime
                price = float(row[1].replace(',', '.'))  # Цена (преобразуем в число и меняем запятую на точку)
                prices.append((date, price))  # Добавляем дату и цену в список
except FileNotFoundError:
    print("Файл не найден.")
except Exception as e:
    print("Произошла ошибка:", e)

# Сортируем цены по датам
sorted_prices = sorted(prices, key=lambda x: x[0])

# Сортируем цены по датам
#sorted_prices = sorted(prices, key=lambda x: x[0])

# Создаем список только с ценами
#prices_only = [price for date, price in sorted_prices]

# Выводим список отсортированных цен
quantity = len(sorted_prices)
logarithmic_returns=[]
h_values = []
h_values_9_14 = []
for i in range(1,quantity):
    log_return = math.log(sorted_prices[i][1] / sorted_prices[i-1][1])
    logarithmic_returns.append(log_return)
length = len(logarithmic_returns)
for j in range(1,length):
     value = logarithmic_returns[j] - logarithmic_returns[j-1]
     h_values.append(value)

h_length = len(h_values)


h_values_decimal = [Decimal(str(value)) for value in h_values]

for item in h_values_decimal:
    print(item)
# Подсчет элементов в каждом интервале
i1 = 0
i2 = 0
i3 = 0

# Вывод результатов
for item in h_values_decimal:
    if item <= Decimal('-0.004135221527782219'):
        i1 += 1
    elif Decimal('-0.004135221527782219') < item <= Decimal('0.006112507775309677'):
        i2 += 1
    else:
        i3 += 1

print(i1)
print(i2)
print(i3)

