import math

def sigma(n, m, f, *args, **kwargs):
    return sum(f(i, *args, **kwargs) for i in range(n, m + 1))

def lambd(T_sr):
    """Интенсивность потока заявок"""
    return 1 / T_sr

def nu(t_obsl):
    """Интенсивность обслуживания"""
    return 1 / t_obsl

def ro(lambd, nu):
    """Загрузка системы"""
    return lambd / nu

def P_(n, ro, i):
    """Вероятность что будет занято i каналов"""
    def f(k, ro):
        return (ro ** k) / math.factorial(k)

    return f(i, ro) / sigma(0, n, f, ro)

def p0(n, ro):
    """Вероятность простоя"""
    # def f(k, ro):
    #     return (ro ** k) / math.factorial(k)

    # return 1 / sigma(0, n, f, ro)
    return P_(n, ro, 0)

def P_otk(ro, n, p0):
    """Вероятность отказа"""
    return ((ro ** n) / (math.factorial(n))) * p0

def Q(P_otk):
    """Относительная пропускная способность"""
    return 1 - P_otk

def A(lambd, Q):
    """Абсолютная пропускная способность"""
    return lambd * Q

def _k(ro, P_otk):
    """Среднее число занятых каналов"""
    return ro * (1 - P_otk)
