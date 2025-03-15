import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



base = 'C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\'
orders = pd.read_csv(base + 'orders.csv')
payments = pd.read_csv(base + 'payments.csv')
plan = pd.read_csv(base + 'plan.csv')

# Преобразуем строки в datetime
payments["paid_at"] = pd.to_datetime(payments["paid_at"]).dt.date
plan["plan_at"] = pd.to_datetime(plan["plan_at"]).dt.date
# Функция для вычисления `late`
def check_late(row, payments):
    order_id = row["order_id"]
    plan_at = row["plan_at"]
    plan_sum_total = row["plan_sum_total"]
    # Все платежи по заказу
    order_payments = payments[payments["order_id"] == order_id].copy()
    # Добавляем столбец "учтен" (сначала все платежи не учтены)
    order_payments["used"] = False
    # Найти все платежи **до текущей даты plan_at**, но не только в этом периоде
    relevant_payments = order_payments[order_payments["paid_at"] <= plan_at]
    # Если платежей вообще нет, значит 100% просрочка
    if relevant_payments.empty:
        return 1
    # Считаем баланс с учетом ранних платежей
    total_paid = 0
    for index, payment in relevant_payments.iterrows():
        if total_paid >= plan_sum_total:
            break  # Если уже оплатили нужную сумму — выходим
        total_paid += payment["paid_sum"]
        order_payments.at[index, "used"] = True  # Отмечаем платеж как учтенный
    # Проверяем, хватило ли денег
    if total_paid >= plan_sum_total:
        return 0  # Нет просрочки
    # Если денег не хватило, проверяем, есть ли платежи **после plan_at** (опоздавшие)
    late_payments = order_payments[~order_payments["used"] & (order_payments["paid_at"] > plan_at)]
    if not late_payments.empty:
        return 1  # Просрочка, так как часть денег пришла поздно
    return 1  # Просрочка (недостаточно денег)
# Рассчитываем `late` для первых 10 строк в `plan`
plan_subset = plan.head(10).copy()  # Берем первые 10 строк
plan["late"] = plan.apply(lambda row: check_late(row, payments), axis=1)
plan.to_csv("C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\new_plan2.csv", index=False)

