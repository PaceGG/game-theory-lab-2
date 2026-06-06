"""Замкнутая многоканальная СМО (система Энгсета)"""

import math

def calculate_engset_smo(n: int, i: int, lmbda: float, mu: float) -> dict:
    """
    Расчет замкнутой СМО Энгсета.
    
    :param n: Количество каналов обслуживания (n >= 1)
    :param i: Общее количество источников заявок (i > n)
    :param lmbda: Интенсивность заявок от одного активного источника
    :param mu: Интенсивность обслуживания одного канала
    """

    alpha = lmbda / mu

    # 1. Расчет инверсной суммы для p0
    inv_p0 = 0.0
    
    # Первая сумма: от 0 до n
    for k in range(n + 1):
        term = (math.factorial(i) / math.factorial(i - k)) * (alpha ** k) / math.factorial(k)
        inv_p0 += term
        
    # Вторая сумма: от n+1 до i (только для многоканальных СМО, если i > n)
    for k in range(n + 1, i + 1):
        term = (math.factorial(i) / math.factorial(i - k)) * (alpha ** k) / (math.factorial(n) * (n ** (k - n)))
        inv_p0 += term

    p0 = 1 / inv_p0

    # 2. Расчет всех вероятностей состояний p_k
    probabilities = []
    for k in range(i + 1):
        if k <= n:
            pk = (math.factorial(i) / math.factorial(i - k)) * (alpha ** k) / math.factorial(k) * p0
        else:
            pk = (math.factorial(i) / math.factorial(i - k)) * (alpha ** k) / (math.factorial(n) * (n ** (k - n))) * p0
        probabilities.append(pk)

    # 3. Среднее число занятых каналов (L_об)
    # Универсальная формула математического ожидания для n каналов
    k_bar = sum(k * probabilities[k] for k in range(n)) + n * (1 - sum(probabilities[k] for k in range(n)))
    l_ob = k_bar

    # 4. Основные характеристики
    a = k_bar * mu  # Абсолютная пропускная способность
    n_akt = a / lmbda
    n_pas = i - n_akt
    l_sist = n_pas
    l_och = l_sist - l_ob
    
    # Вероятность наличия очереди
    p_och = sum(probabilities[k] for k in range(n + 1, i + 1))
    p_akt_src = n_akt / i

    # Временные показатели (Формулы Литтла через среднюю интенсивность потока A)
    t_ob = 1 / mu
    t_och = l_och / a if a > 0 else 0.0
    t_sist = t_och + t_ob

    return {
        "Тип системы": "Одноканальная замкнутая" if n == 1 else f"Многоканальная замкнутая ({n} кан.)",
        "Коэффициент загрузки источника (alpha)": alpha,
        "Предельные вероятности состояний (p_k)": [p for p in probabilities],
        "Вероятность p0 (все свободны)": p0,
        "Вероятность наличия очереди (Pоч)": p_och,
        "Абсолютная пропускная способность (A)": a,
        "Среднее число активных источников (Nакт)": n_akt,
        "Среднее число пассивных источников (Nпас)": n_pas,
        "Среднее число заявок под обслуживанием (Lоб)": l_ob,
        "Среднее число заявок в очереди (Lоч)": l_och,
        "Среднее число заявок в системе (Lсист)": l_sist,
        "Стационарный коэф. активности источника (Pакт)": p_akt_src,
        "Среднее время ожидания в очереди (Tоч)": t_och,
        "Среднее время обслуживания (Tоб)": t_ob,
        "Среднее время в системе (Tсист)": t_sist
    }
