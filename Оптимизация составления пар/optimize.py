import numpy as np
from scipy.optimize import minimize

# Целевая функция для минимизации
def objective_function(x):
    alpha, beta, gamma, delta = x
    return alpha * 2.85 + beta * 2.73 + gamma * 1.87 + delta * 2.62

# Ограничения
def constraint_sum(x):
    return np.sum(x) - 1.0

def constraint_delta_alpha(x):
    return x[3] - x[0] - 1e-6  # delta - alpha > 0

def constraint_delta_beta(x):
    return x[3] - x[1] - 1e-6  # delta - beta > 0

def constraint_delta_gamma(x):
    return x[3] - x[2] - 1e-6  # delta - gamma > 0

# Начальное приближение с малыми положительными значениями

x3 = np.array([0.2, 0.2, 0.2, 0.4])
# Ограничения
constraints = [
    {'type': 'eq', 'fun': constraint_sum},
    {'type': 'ineq', 'fun': constraint_delta_alpha},
    {'type': 'ineq', 'fun': constraint_delta_beta},
    {'type': 'ineq', 'fun': constraint_delta_gamma}
]

# Ограничения для коэффициентов (убираем возможность нулевых значений)
bounds = [(1e-6, 1), (1e-6, 1), (1e-6, 1), (1e-6, 1)]

# Оптимизация
result = minimize(objective_function, x3, method='SLSQP', bounds=bounds, constraints=constraints)


# Сортировка коэффициентов по убыванию


# Вывод результатов
# Вывод результатов
print(f"Оптимальные значения весовых коэффициентов:")
print(f"alpha = {result.x[0]}")
print(f"beta = {result.x[1]}")
print(f"gamma = {result.x[2]}")
print(f"delta = {result.x[3]}")
print(f"Минимальная сумма = {result.fun}")
print(result.x[1] > result.x[0] )

