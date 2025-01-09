import numpy as np

# Пример ряда логарифмических доходностей
logarithmic_returns = [0.01, 0.02, -0.005, 0.015]

def calculate_hirsch_coefficient(logarithmic_returns):
    # Рассчитываем среднее значение логарифмических доходностей
    total_log_return = np.sum(logarithmic_returns)
    # Рассчитываем количество периодов
    num_periods = len(logarithmic_returns)
    # Рассчитываем среднюю логарифмическую доходность
    mean_log_return = total_log_return / num_periods
    
    # Рассчитываем разность между каждой логарифмической доходностью и средним значением
    deviations = logarithmic_returns - mean_log_return
    # Возводим разности в куб и суммируем
    sum_cubed_deviations = np.sum(deviations**3)/num_periods
    
    # Возводим разности в квадрат и суммируем
    sum_squared_deviations = np.sum(deviations**2)/num_periods
    
    # Рассчитываем коэффициент Херша
    hirsch_coefficient = sum_cubed_deviations / ((sum_squared_deviations)**(3/2))
    return hirsch_coefficient
    

# Вызываем функцию для расчета коэффициента Херша
hirsch_coefficient = calculate_hirsch_coefficient(logarithmic_returns)
print("Коэффициент Херша (H):", hirsch_coefficient)
