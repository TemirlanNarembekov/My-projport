import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from datetime import datetime
from scipy.stats import norm
# Задайте путь к CSV файлу
file_path = 'C:\\Users\\user\\Desktop\\КУРСОВАЯ\\data_2009-2024.csv'

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
prices_only = [price for date, price in sorted_prices]

quantity = len(sorted_prices)
logarithmic_returns=[]
for i in range(1,quantity):
    log_return = math.log(prices_only[i] / prices_only[i-1])
    logarithmic_returns.append(log_return)
logarithmic_returns_array = np.array(logarithmic_returns)
length = len(logarithmic_returns_array)


def map_elements_to_sorted_indices(arr):
    sorted_indices = sorted(range(len(arr)), key=lambda x: arr[x])
    mapped_indices = [sorted_indices.index(i) for i in range(len(arr))]
    return mapped_indices

def add_one_to_mapped_indices(mapped_indices):
    return [index + 1 for index in mapped_indices]

arr1 = [23,21,25,22,24]
arr2 = list(range(1, 180))

mapped_indices = map_elements_to_sorted_indices(arr1)
Ranks = add_one_to_mapped_indices(mapped_indices)

def R_statistics(ranks):
    overall = 0
    for i in range(0, 4):#178
        factor1 = ranks[i] - 3#90
        #print(factor1)
        factor2 = ranks[i+1] - 3
        #print(factor2)
        product = factor1*factor2
        #print(product)
        overall+=product
        #print(overall)
    return overall


alpha = 0.01 #0.00558659217877
critical_value = norm.ppf(1 - alpha/2)
print("критические значения",critical_value)  # Output: 1.96



R = R_statistics(Ranks)
D_R = 1270233404
R_star = R/(D_R**(0.5))
R_double_star = R_star + 1.1216*179**(-0.523)

print(R_double_star)
print(R)