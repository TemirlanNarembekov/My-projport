from statsmodels.stats.stattools import durbin_watson
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import csv
import math
from datetime import datetime
from scipy.stats import ks_2samp
from scipy.stats import kruskal
import statsmodels.stats.multitest as multitest
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
from statsmodels.tsa.stattools import adfuller
from arch import arch_model

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
# Задаем данные
df = pd.DataFrame(logarithmic_returns_array, columns=['LogReturns'])

nAnS = df.isna().sum()

mean = df['LogReturns'].mean()
std_dev = df['LogReturns'].std()

# Выбросы более чем на 3 стандартных отклонения от среднего
outliers = df[(df['LogReturns'] < mean - 3 * std_dev) | (df['LogReturns'] > mean + 3 * std_dev)]
print(outliers)

df_cleaned = df[(df['LogReturns'] >= mean - 3 * std_dev) & (df['LogReturns'] <= mean + 3 * std_dev)]
# Выполняем тест Дики-Фуллера на стационарность
# result = adfuller(df['LogReturns'])

# # Выводим результаты теста
# print('ADF Statistic:', result[0])
# print('p-value:', result[1])
# print('Critical Values:', result[4])

# # Интерпретация результатов
# if result[1] < 0.05:
#     print("Ряд стационарен (отклоняем нулевую гипотезу).")
# else:
#     print("Ряд не стационарен (не отклоняем нулевую гипотезу).")


# Ваши логарифмические доходности

# Построение GARCH(1,1) модели
scaled_df = df_cleaned * 100
model = arch_model(scaled_df, vol='Garch', p=1, q=1, mean='Zero')
garch_result = model.fit()

# Вывод результатов
print(garch_result.summary())