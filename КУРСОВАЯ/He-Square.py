import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from datetime import datetime
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

# Выводим цены в порядке возрастания даты
for date, price in sorted_prices:
    print(f"Дата: {date.strftime('%d.%m.%Y')}, Цена: {price}")
# Создаем список только с ценами
prices_only = [price for date, price in sorted_prices]
for price1 in prices_only:
    print(price1)
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

# Заданные наблюдения
observations = h_values#array([-10.33, -1, 11, 4, 0,67,-0.0577,-99.1,100,200])

# Сортируем данные в порядке возрастания
observations = np.sort(observations)
for item in observations:
    print(item)
# Разделение на три интервала
interval_size = len(observations) // 3
extra = len(observations) % 3

observations_intervals = []
start_index = 0

for i in range(3):
    end_index = start_index + interval_size + (1 if i < extra else 0)
    observations_intervals.append(observations[start_index:end_index])
    start_index = end_index

# Вывод интервалов
print("Интервалы:")
print(f"Интервал 1: (-inf, {observations_intervals[0][-1]}]")
print(f"Интервал 2: ({observations_intervals[0][-1]}, {observations_intervals[1][-1]}]")
print(f"Интервал 3: ({observations_intervals[1][-1]}, +inf)")

# Вывод списка наблюдений в каждом интервале
print("\nНаблюдения в каждом интервале:")
for i, interval in enumerate(observations_intervals, start=1):
    print(f"Интервал {i}: {interval}")
print("\nКоличество наблюдений в каждом интервале:")
for i, interval in enumerate(observations_intervals, start=1):
    print(f"Интервал {i}: {len(interval)}")