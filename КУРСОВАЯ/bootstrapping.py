import numpy as np
from scipy.stats import skew
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
length = len(logarithmic_returns_array)

#for item in logarithmic_returns_array:
 #   print(item)

# Создаем подвыборки
sample_sub1 = logarithmic_returns_array[:56]
sample_sub2 = logarithmic_returns_array[56:58]  # Исправлено извлечение двух элементов
sample_sub3 = logarithmic_returns_array[58:74]
sample_sub4 = logarithmic_returns_array[74:131]
sample_sub5 = logarithmic_returns_array[131:152]
sample_sub6 = logarithmic_returns_array[152:157]
sample_sub7 = logarithmic_returns_array[157:179]

# Функция бутстрапа для вычисления доверительного интервала коэффициента асимметрии
def bootstrap_skewness(data, num_samples=1000, tolerance=1e-8):
    skewness_values = []
    
    # Проверяем вариативность данных
    if np.std(data) < tolerance or len(np.unique(data)) == 1:
        print("Данные почти идентичны, асимметрия может быть неинформативной.")
        return [np.nan, np.nan]  # Возвращаем NaN, если данные не вариативны или идентичны

    for _ in range(num_samples):
        sample = np.random.choice(data, size=len(data), replace=True)  # Бутстрап выборка
        skewness_values.append(skew(sample))
    
    return np.percentile(skewness_values, [2.5, 97.5])  # 95% доверительный интервал
# Доверительные интервалы для коэффициентов асимметрии
ci_subset1 = bootstrap_skewness(sample_sub1)
ci_subset2 = bootstrap_skewness(sample_sub2)
ci_subset3 = bootstrap_skewness(sample_sub3)
ci_subset4 = bootstrap_skewness(sample_sub4)
ci_subset5 = bootstrap_skewness(sample_sub5)
ci_subset6 = bootstrap_skewness(sample_sub6)
ci_subset7 = bootstrap_skewness(sample_sub7)
# Вывод доверительных интервалов для каждой подвыборки
confidence_intervals = [ci_subset1, ci_subset2, ci_subset3, ci_subset4, ci_subset5, ci_subset6, ci_subset7]

for i, ci in enumerate(confidence_intervals, start=1):
    print(f"95% доверительный интервал асимметрии для подвыборки {i}: {ci[0]} - {ci[1]}")
# print(f"95% CI for skewness of subset1: {ci_subset1}")
# print(f"95% CI for skewness of subset2: {ci_subset2}")

# Список доверительных интервалов для подвыборок
confidence_intervals = [ci_subset1, ci_subset2, ci_subset3, ci_subset4, ci_subset5, ci_subset6, ci_subset7]

# Сравнение доверительных интервалов между всеми подвыборками

# for i in range(len(confidence_intervals)):
#     for j in range(i + 1, len(confidence_intervals)):
#         ci_i = confidence_intervals[i]
#         ci_j = confidence_intervals[j]
        
#         # Проверка пересечения доверительных интервалов
#         if ci_i[1] < ci_j[0] or ci_j[1] < ci_i[0]:
#             print(f"Коэффициенты асимметрии значимо различаются в подвыборках {i+1} и {j+1}.")
#         else:
#             print(f"Коэффициенты асимметрии статистически неотличимы в подвыборках {i+1} и {j+1}.")




# print(ci_subset1[0])
# print(ci_subset1[1])
# print("////")
# print(ci_subset2[0])
# print(ci_subset2[1])
# print("////")
# print(ci_subset3[0])
# print(ci_subset3[1])
# print("////")
# print(ci_subset4[0])
# print(ci_subset4[1])
# print("////")
# print(ci_subset5[0])
# print(ci_subset5[1])
# print("////")
# print(ci_subset6[0])
# print(ci_subset6[1])
# print("////")
# print(ci_subset7[0])
# print(ci_subset7[1])

