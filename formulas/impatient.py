"""Многоканальная СМО с нетерпеливыми заявками"""

import math

def calculate_impatient_smo(n: int, lmbda: float, mu: float, omega: float, epsilon: float = 1e-7) -> dict:
    """
    Расчет характеристик многоканальной СМО с "нетерпеливыми" заявками.
    
    :param n: Количество каналов обслуживания (n > 0)
    :param lmbda: Интенсивность входящего потока заявок
    :param mu: Интенсивность обслуживания одного канала
    :param omega: Интенсивность ухода заявки из очереди
    :param epsilon: Точность расчета бесконечного ряда для p0
    :return: Словарь с характеристиками СМО
    """
    rho = lmbda / mu
    beta = omega / mu

    # 1. Расчет базовой суммы для каналов (от k = 0 до n)
    sum_channels = sum((rho ** k) / math.factorial(k) for k in range(n + 1))

    # 2. Расчет бесконечного ряда для очереди (с заданной точностью)
    sum_queue = 0.0
    m = 1
    current_term = 1.0
    denominator_product = 1.0
    p_n_multiplier = (rho ** n) / math.factorial(n)

    while True:
        # Считаем произведение (n + 1*beta) * (n + 2*beta) * ... * (n + m*beta)
        denominator_product *= (n + m * beta)
        # Очередной член ряда внутри суммы по m
        current_term = (rho ** m) / denominator_product
        
        # Если член ряда стал ничтожно мал, останавливаемся
        if current_term < epsilon:
            break
            
        sum_queue += current_term
        m += 1

    # Полное выражение под знаком инверсии для p0
    p0 = 1 / (sum_channels + p_n_multiplier * sum_queue)

    # 3. Расчет вероятностей состояний каналов p_k (от 0 до n) для вычисления k_bar
    probabilities_channels = [(rho ** k) / math.factorial(k) * p0 for k in range(n)]

    # 4. Среднее число занятых каналов (k_bar / L_об)
    # Формула: sum_{k=0}^{n-1} k*p_k + n * (1 - sum_{k=0}^{n-1} p_k)
    sum_k_pk = sum(k * p_k for k, p_k in enumerate(probabilities_channels))
    sum_pk_under_n = sum(probabilities_channels)
    k_bar = sum_k_pk + n * (1 - sum_pk_under_n)

    # 5. Расчет остальных характеристик эффективности
    l_ob = k_bar
    l_och = (rho - k_bar) / beta
    l_sist = l_och + l_ob

    q = k_bar / rho  # Относительная пропускная способность (P_об)
    a = lmbda * q    # Абсолютная пропускная способность
    p_ux = 1 - q     # Вероятность ухода заявки из очереди

    # Временные показатели (Формулы Литтла)
    t_och = l_och / lmbda
    t_ob_fact = l_ob / a
    t_sist = l_sist / lmbda

    return {
        "Параметр загрузки (rho)": rho,
        "Приведенная интенсивность ухода (beta)": beta,
        "Вероятность p0 (система свободна)": p0,
        "Среднее число занятых каналов (Lоб)": l_ob,
        "Среднее число заявок в очереди (Lоч)": l_och,
        "Среднее число заявок в системе (Lсист)": l_sist,
        "Вероятность быть обслуженной (Q)": q,
        "Вероятность ухода из очереди (Pух)": p_ux,
        "Абсолютная пропускная способность (A)": a,
        "Среднее время в очереди (Tоч)": t_och,
        "Среднее время обслуживания (Tоб)": t_ob_fact,
        "Среднее время в системе (Tсист)": t_sist,
        "Количество учтенных членов ряда очереди": m - 1
    }