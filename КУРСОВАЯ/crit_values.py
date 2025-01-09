import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
import matplotlib.pyplot as plt

# Функция для симуляции критических значений Дарбина-Уотсона
def simulate_dw_critical_values(n, k, num_simulations=10000, alpha=0.01):
    """
    Симулирует распределение статистики Дарбина-Уотсона для модели с заданным числом наблюдений и параметров.
    
    :param n: Количество наблюдений
    :param k: Количество параметров модели (включая свободный член)
    :param num_simulations: Количество симуляций для оценки критических значений
    :param alpha: Уровень значимости (по умолчанию 0.01)
    :return: Кортеж с нижней (d_L) и верхней (d_U) границей критического значения
    """
    dw_statistics = []

    # Симулируем остатки случайных нормальных данных для модели с k параметрами
    for _ in range(num_simulations):
        residuals = np.random.normal(size=n)  # Симуляция остатков
        dw_stat = durbin_watson(residuals)
        dw_statistics.append(dw_stat)
    
    # Преобразуем список в массив
    dw_statistics = np.array(dw_statistics)
    
    # Находим критические значения по процентилям
    d_L = np.percentile(dw_statistics, alpha * 100)
    d_U = np.percentile(dw_statistics, (1 - alpha) * 100)
    
    return d_L, d_U

# Пример использования для 179 наблюдений и 26 параметров
n = 179  # Количество наблюдений
k = 26   # Количество параметров (включая свободный член)

# Симуляция критических значений Дарбина-Уотсона
d_L, d_U = simulate_dw_critical_values(n, k)
print(d_L, d_U)
# Degrees of freedom and significance level
df1 = 29
df2 = 18
alpha = 0.05
alpha1 = 0.01
n = 179

# Critical value from the Chi-Square distribution table
critical_value1 = stats.chi2.ppf(1 - alpha, df1)
critical_value2 = stats.t.ppf(1-alpha/2, df2)

print(critical_value2)
# critical_value_ks = stats.kstwobign.ppf(alpha1)
# print(critical_value_ks)
# print(critical_value_ks/np.sqrt(n))



