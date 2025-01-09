import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
import seaborn as sns
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
prices_only = [price for date, price in sorted_prices]


quantity = len(sorted_prices)
logarithmic_returns=[]
for i in range(1,quantity):
    log_return = math.log(prices_only[i] / prices_only[i-1])
    logarithmic_returns.append(log_return)

logarithmic_returns_array = np.array(logarithmic_returns)

# for item in logarithmic_returns_array:
#     print(item)
# Пример массива


# Находим наименьший элемент
minimum_value = min(logarithmic_returns_array)
maximum_value = max(logarithmic_returns_array)

# print("Наименьший элемент массива:", minimum_value)
# print("Наибольший элемент массива:", maximum_value)


# Параметры нормального распределения
mean = 0        # Среднее значение
std_dev = 1     # Стандартное отклонение
size = 179      # Размер массива

# Генерация массива с нормально распределенными данными
normal_distribution_array = np.random.normal(loc=mean, scale=std_dev, size=size)

sample1 = np.random.normal(loc=mean, scale=std_dev, size=size)

sample2 = np.random.normal(loc=mean, scale=std_dev, size=size+86)


stat, p_value = stats.ks_2samp(sample1,sample2)

print(f"K-S test statistic: {stat}, p-value: {p_value}")

print(p_value < 0.05)

