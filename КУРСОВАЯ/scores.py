import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from datetime import datetime
from scipy.stats import ks_2samp
from scipy.stats import kruskal
import statsmodels.stats.multitest as multitest
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



# sample_sub1 = logarithmic_returns_array[:56]
# sample_sub2 = sample_sub2 = logarithmic_returns_array[56:58]
# sample_sub3 = logarithmic_returns_array[58:74]
# sample_sub4 = logarithmic_returns_array[74:131]
# sample_sub5 = logarithmic_returns_array[131:152]
# sample_sub6 = logarithmic_returns_array[152:157]
# sample_sub7 = logarithmic_returns_array[157:179]

# def scores(logarithmic):
#     mean = np.mean(logarithmic)
#     return mean
    
# m1 = scores(sample_sub1)
# m2 = scores(sample_sub2)
# m3 = scores(sample_sub3)
# m4 = scores(sample_sub4)
# m5 = scores(sample_sub5)
# m6 = scores(sample_sub6)
# m7 = scores(sample_sub7)


# Вызываем функцию для расчета коэффициента Херша
#print("M1",m1)
#print("M2",m2)
#print("M3",m3)
#print("M4",m4)
#print("M5",m5)
#print("M6",m6)
#print("M7",m7)


# f_stat, p_value = stats.f_oneway(sample_sub1, sample_sub2, sample_sub3, sample_sub4, sample_sub5, sample_sub6, sample_sub7)
# #print(f"ANOVA F-statistic: {f_stat}, p-value: {p_value}")

# stat, p_value_l = stats.levene(sample_sub1, sample_sub2, sample_sub3, sample_sub4, sample_sub5, sample_sub6, sample_sub7)
# #print(f"Levene test statistic: {stat}, p-value: {p_value_l}")

# samples = [sample_sub1, sample_sub2, sample_sub3, sample_sub4, sample_sub5, sample_sub6, sample_sub7]

# Функция для проведения теста Колмогорова-Смирнова для всех пар подвыборок
# def ks_test(samples):
#     num_samples = len(samples)
#     p_values = []
#     pairs = []  # Список для хранения пар индексов выборок

#     for i in range(num_samples):
#         for j in range(i + 1, num_samples):
#             _, p_value = ks_2samp(samples[i], samples[j])
#             p_values.append(p_value)
#             pairs.append((i, j))  # Сохраняем индексы пар

#     return p_values, pairs

# # Проведение теста
# p_values, pairs = ks_test(samples)

# # Корректировка p-значений методом Бонферрони
# corrected_p_values = multitest.multipletests(p_values, method='bonferroni')[1]

# # Вывод результатов
# for idx, p_value in enumerate(p_values):
#     pair = pairs[idx]
#     i, j = pair
#     print(f"Выборки {i + 1} и {j + 1}:")
#     print(f"  Исходное p-значение: {p_value:.4f}, Скорректированное p-значение: {corrected_p_values[idx]:.4f}")
#     if corrected_p_values[idx] < 0.05:
#         print(f"  Выборки {i + 1} и {j + 1} значимо различаются.")
#     else:
#         print(f"  Выборки {i + 1} и {j + 1} статистически неотличимы.")


sample1 = logarithmic_returns_array[:80]
sample2 = logarithmic_returns_array[80:179]

stat, p_value_s = stats.ks_2samp(sample1,sample2)

print(f"K-S test statistic: {stat}, p-value: {p_value_s}")

print(p_value_s < 0.01)
print(p_value_s< 0.05)
# statistic, p_value_ll = stats.kstest(logarithmic_returns_array, 'norm', args=(mean, std))

# print(p_value_ll < 0.05)
# print(p_value_ll == p_value)


