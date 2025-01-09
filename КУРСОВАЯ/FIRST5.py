import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from datetime import datetime
# Задайте путь к CSV файлу
file_path = 'C:\\Users\\user\\Desktop\\КУРСОВАЯ\\may2019-april2024.csv'

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

# Выводим цены в порядке возрастания даты
for date, price in sorted_prices:
    print(f"Дата: {date.strftime('%d.%m.%Y')}, Цена: {price}")
# Сортируем цены по датам
#sorted_prices = sorted(prices, key=lambda x: x[0])

# Создаем список только с ценами
#prices_only = [price for date, price in sorted_prices]

# Выводим список отсортированных цен
quantity = len(sorted_prices)
logarithmic_returns=[]
h_values = []
for i in range(1,quantity):
    log_return = math.log(sorted_prices[i][1] / sorted_prices[i-1][1])
    logarithmic_returns.append(log_return)
length = len(logarithmic_returns)
for j in range(1,length):
     value = logarithmic_returns[j] - logarithmic_returns[j-1]
     h_values.append(value)

h_length = len(h_values)

def count_elements(sequence):
    less_than_zero = 0
    greater_than_zero = 0
    equal_to_zero = 0

    for num in sequence:
        if num < 0:
            less_than_zero += 1
        elif num > 0:
            greater_than_zero += 1
        else:
            equal_to_zero += 1

    return less_than_zero, greater_than_zero, equal_to_zero

# Пример использования
seq = [12, 112,0,-1]
less_than_zero, greater_than_zero, equal_to_zero = count_elements(h_values)
print("Количество элементов меньше 0:", less_than_zero)
print("Количество элементов больше 0:", greater_than_zero)
print("Количество элементов равных 0:", equal_to_zero)

