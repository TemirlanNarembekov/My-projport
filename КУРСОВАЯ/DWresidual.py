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



# Загрузка данных

from statsmodels.stats.diagnostic import acorr_ljungbox
#create dataset
data = np.array(logarithmic_returns)  
df = pd.DataFrame({'LogReturns': data})
df['Time'] = np.arange(len(data))  # Создаем временной индекс
for item in np.arange(len(data)):
    print(item)
X = df[['Time']]  # Используем временной индекс в качестве предиктора
y = df['LogReturns']
time = np.arange(len(data))
df = pd.DataFrame({'LogReturns': data,
                   'Time': time })
X = sm.add_constant(X)
# Создание и обучение модели
model = sm.OLS(y, X).fit()
residuals = model.resid

print(model.summary())
# acorr_ljungbox(model.resid, lags=[13, 14], model_df=2, return_df=True)

################# ljung_box_results = acorr_ljungbox(logarithmic_returns_array, lags=[13, 14],model_df=13, return_df=True)

# print(acorr_ljungbox(model.resid, lags=[13, 14], model_df=2, return_df=True))



# dw_statistic = durbin_watson(residuals)
# print(f"Durbin-Watson statistic: {dw_statistic}")

# print(model.summary())

# #fit multiple linear regression model
# model = ols(data = logarithmic_returns_array).fit()
# #perform Durbin-Watson test
# durbin_watson(model.resid)
# # print(durbin_watson(model.resid))