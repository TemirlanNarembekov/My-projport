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

# Зависимая переменная Y: логарифмическая доходность в следующий период
df['Y'] = df['LogReturns'].shift(-1)  # Сдвиг на один период вперёд

# Создаем лаговые переменные (всего 13 лагов: от r_t до r_{t-12})
for i in range(1, 14):  # 13 лагов
    df[f'X{i}'] = df['LogReturns'].shift(i)

# Удаляем строки с отсутствующими значениями
df = df.dropna()

# Зависимая переменная
Y = df['Y']

# Независимые переменные: 13 лагов
X = df.drop(columns=['Y'])

# Добавляем константу (свободный член)
X = sm.add_constant(X)

# Шаг 1: Строим начальную модель с полным набором лагов
initial_model = sm.OLS(Y, X).fit()

# Шаг 2: Отбираем только значимые переменные (p-value < 0.05)
significant_predictors = initial_model.pvalues[initial_model.pvalues < 0.01].index

# Удаляем из списка зависимую переменную 'const', чтобы сохранить её в модели
significant_predictors = [var for var in significant_predictors if var != 'const']

# Создаем новый набор данных только с константой и значимыми предикторами
X_significant = sm.add_constant(df[significant_predictors])

# Шаг 3: Строим новую модель только с оставшимися предикторами
final_model = sm.OLS(Y, X_significant).fit()

residuals = final_model.resid

# Выводим результаты итоговой модели
print(final_model.summary())
# bg_test = acorr_breusch_godfrey(final_model, nlags=2)
# print(f"P-значение теста: {bg_test[1]}")