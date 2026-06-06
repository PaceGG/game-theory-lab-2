"""Многоканальная СМО с неограниченной очередью"""
import math

import math

def calculate_p0(rho: float, n: int) -> float:
    """
    Расчет вероятности простоя системы (p0).
    """
    
    # Расчет суммы от k=0 до n-1
    sum_part = sum((rho ** k) / math.factorial(k) for k in range(n))
    
    # Расчет второго слагаемого в скобках
    tail_part = (rho ** n) / math.factorial(n) * (1 / (1 - rho / n))
    
    # Возвращаем значение в степени -1
    return 1 / (sum_part + tail_part)


def calculate_p_och(rho: float, n: int, p0: float = None) -> float:
    """
    Расчет вероятности образования очереди (P_оч).
    """
    if p0 is None:
        p0 = calculate_p0(rho, n)
        
    return ((rho ** n) / math.factorial(n)) * (p0 / (1 - rho / n))


def calculate_l_och(rho: float, n: int, p0: float = None) -> float:
    """
    Расчет среднего числа требований в очереди (L_оч).
    """
    if p0 is None:
        p0 = calculate_p0(rho, n)
        
    denominator = n * math.factorial(n)
    return ((rho ** (n + 1)) / denominator) * (p0 / ((1 - rho / n) ** 2))


def calculate_l_sist(rho: float, n: int, p0: float = None) -> float:
    """
    Расчет среднего числа требований в системе (L_сист).
    """
    l_och = calculate_l_och(rho, n, p0)
    return l_och + rho
