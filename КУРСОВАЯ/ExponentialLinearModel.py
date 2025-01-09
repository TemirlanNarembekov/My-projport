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
from statsmodels.regression.linear_model import OLS
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

df = pd.DataFrame(logarithmic_returns_array, columns=['LogReturns'])

# Зависимая переменная Y: логарифмическая доходность в следующий период
df['Y'] = df['LogReturns'].shift(-1)  # Сдвиг на один период вперёд

# Создаем лаговые переменные (всего 13 лагов: от r_t до r_{t-12})
for i in range(1, 14):  # 13 лагов
    df[f'X{i}'] = df['LogReturns'].shift(i)

# Удаляем строки с отсутствующими значениями
df = df.dropna()

# Создаем матрицу признаков Фурье
n = len(df)  # Количество наблюдений
fourier_terms = 6  # Количество гармоник
t = np.arange(n)

# Матрица признаков для модели Фурье
X_fourier = pd.DataFrame(index=df.index)
for k in range(1, fourier_terms + 1):
    X_fourier[f'sin_{k}'] = np.sin(2 * np.pi * k * t / n)
    X_fourier[f'cos_{k}'] = np.cos(2 * np.pi * k * t / n)

# Соединяем лаговые переменные и гармонические признаки
X = pd.concat([df[[f'X{i}' for i in range(1, 14)]], X_fourier], axis=1)

# Добавляем константу (свободный член)
X = sm.add_constant(X)

# Зависимая переменная
Y = df['Y']

# Построение модели
model = OLS(Y, X)
results = model.fit()

# Выводим результаты модели
print(results.summary())