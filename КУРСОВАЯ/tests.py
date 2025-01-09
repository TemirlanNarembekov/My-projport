from scipy.stats import lognorm
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
from scipy.stats import t
import warnings
from scipy.stats import weibull_min
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



sample_sub1 = logarithmic_returns_array[:80]
# sample_sub2 = sample_sub2 = logarithmic_returns_array[56:58]
# sample_sub3 = logarithmic_returns_array[58:74]
sample_sub2 = logarithmic_returns_array[80:179]
# sample_sub5 = logarithmic_returns_array[131:152]
# sample_sub6 = logarithmic_returns_array[152:157]
# sample_sub7 = logarithmic_returns_array[157:179]

#тест Колмогорова-Смирнова на логнормальное распределение 
# shift_value = abs(min(logarithmic_returns_array)) + 0.0001  # Добавим небольшое положительное число для избегания нуля
# log_returns_shifted = logarithmic_returns_array + shift_value
# shape, loc, scale = lognorm.fit(log_returns_shifted,floc = 0)
# stat, p_value = stats.kstest(log_returns_shifted, 'lognorm', args=(shape, loc, scale))
# print(f'K-S тест для логнормального распределения: статистика = {stat}, p-значение = {p_value}')

# df, loc, scale = t.fit(logarithmic_returns_array)
# stat, p_value = stats.kstest(logarithmic_returns_array, 't', args=(df, loc, scale))
# print(f'K-S тест для распределения Стьюдента: статистика = {stat}, p-значение = {p_value}')



# Ваши данные

# def cramer_mises_test(data, dist, *args):
#     """
#     Тест Крамера — Мизеса для проверки соответствия данных распределению.
    
#     :param data: Массив данных.
#     :param dist: Имя распределения из scipy.stats.
#     :param args: Параметры распределения.
#     :return: Значение статистики теста и p-значение.
#     """
#     # Эмпирическая функция распределения
#     ecdf = np.arange(1, len(data) + 1) / len(data)
    
#     # Параметры для теоретического распределения
#     sorted_data = np.sort(data)
#     cdf_theoretical = dist.cdf(sorted_data, *args)
    
#     # Расчет статистики теста Крамера — Мизеса
#     statistic = np.sum((ecdf - cdf_theoretical) ** 2) / len(data)
    
#     # Здесь мы просто демонстрируем расчет статистики. P-значение нужно
#     # вычислять с помощью специальных таблиц или численных методов.
#     # Для демонстрации будем использовать p-значение из Kolmogorov-Smirnov теста.
#     ks_stat, ks_p_value = stats.kstest(data, dist.name, args=args)
    
#     return statistic, ks_p_value

# # Пример данных: замените на ваши данные


# # Подгонка распределения Стьюдента
# df = stats.t.fit(logarithmic_returns_array)[0]  # Например, степени свободы равны 3
# cramer_mises_stat, cramer_mises_p_value = cramer_mises_test(logarithmic_returns_array, stats.t, df)
# print("Тест Крамера — Мизеса — Смирнова для распределения Стьюдента:")
# print(f"Статистика: {cramer_mises_stat:.4f}")
# print(f"P-значение: {cramer_mises_p_value:.4f}")


#Подгонка распределения Вейбулла
# c, loc, scale = weibull_min.fit(sample_sub1)
shape, loc, scale = stats.weibull_min.fit(sample_sub2)
random_samples = stats.weibull_min.rvs(shape, loc=loc, scale=scale, size=len(sample_sub2))
# print('Параметр формы:',shape)
# print('Параметр сдвига:',loc)
# print('Параметр масштаба:',scale)
ks_statistic, p_value = stats.ks_2samp(sample_sub2, random_samples)
# ks_statistic, p_value = stats.kstest(sample_sub2, 'weibull_min', args=(shape, loc, scale))
print(f'KS Statistic: {ks_statistic}')
print(f'P-value: {p_value}')



# # Тест Колмогорова-Смирнова двух подвыборок выборки
# ks_stat, ks_p_value = stats.ks_2samp(sample_sub1, sample_sub2)
# print("Тест Колмогорова-Смирнова для двух выборок:")
# print(f"Статистика K-S: {ks_stat}")
# print(f"P-значение: {ks_p_value}")



# from statsmodels.sandbox.stats.runs import runstest_1samp

# # Применение теста на случайность на логарифмические доходности
# z_stat, p_value = runstest_1samp(logarithmic_returns_array, correction=True)
# print(f'Z-статистика: {z_stat}, p-значение: {p_value}')


from statsmodels.stats.diagnostic import acorr_ljungbox

# Применение теста Льюнг-Бокса на логарифмические доходности
# ljung_box_results = acorr_ljungbox(logarithmic_returns_array, lags=[13, 14], return_df=True)
# # print(ljung_box_results)

#perform Kolmogorov-Smirnov test
# ks_2samp(sample_sub1, sample_sub2)
# print("KS:",ks_2samp(sample_sub1, sample_sub2))
# print(7.76289013388451e-06 < 0.01)