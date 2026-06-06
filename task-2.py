import math
from formulas.waiting import (
    calculate_p0, 
    calculate_l_och, 
    calculate_l_sist,
    calculate_p_och
)

lambda_day = 350 # lambda 
mu = 1440 / 10 # 1440 / t (заявок в сутки)
alpha = 7 # alpha
n = 3

rho = lambda_day / mu

# 1 Определить минимальное количество каналов обслуживания kmin, при
# котором очередь не будет расти до бесконечности (условие стационарности:
# ρ/n < 1), а также рассчитать соответствующие характеристики обслуживания
# при полученном kmin:
#     o предельные вероятности состояний;
#     o среднее число заявок в очереди и в системе;
#     o среднее время ожидания и пребывания в системе.

# условие стационарности: ρ/n < 1 => n > ρ
n_min = int(math.floor(rho) + 1)
print(f"Минимальное количество каналов обслуживания kmin, при котором очередь не будет расти до бесконечности: {n_min}")

p0_min = calculate_p0(rho, n_min)
l_och_min = calculate_l_och(rho, n_min, p0_min)
l_sist_min = calculate_l_sist(rho, n_min, p0_min)

# По закону Литтла: T = L / lambda
T_och_min = l_och_min / lambda_day   # в сутках
T_sist_min = l_sist_min / lambda_day # в сутках

print(f"Вероятность простоя p0: {p0_min:.4f}")
print(f"Среднее число заявок в очереди L_оч: {l_och_min:.4f}")
print(f"Среднее число заявок в системе L_сист: {l_sist_min:.4f}")
print(f"Среднее время ожидания T_оч: {T_och_min * 24 * 60:.2f} минут ({T_och_min:.5f} суток)")
print(f"Среднее время пребывания T_сист: {T_sist_min * 24 * 60:.2f} минут ({T_sist_min:.5f} суток)")
print()


# 2 Найти оптимальное количество каналов kopt, при котором относительная
# величина затрат Cотн, связанная с издержками на содержание каналов и с
# пребыванием заявок в очереди, будет минимальной.
# Функция затрат задается как C(k) = k/lambda + alpha*T_обсл

# Согласно условию, минимизируем функцию: C(n) = n/lambda + alpha * T_ожидания.

def calculate_costs(n: int, rho_val: float, lambda_val: float, alpha_val: float) -> float:
    if n <= rho_val:
        return float('inf')
    p0 = calculate_p0(rho_val, n)
    l_och = calculate_l_och(rho_val, n, p0)
    t_och = l_och / lambda_val
    return (n / lambda_val) + alpha_val * t_och

n_opt = n_min
min_cost = calculate_costs(n_min, rho, lambda_day, alpha)

# Перебираем каналы вверх от n_min, пока затраты падают
for n_test in range(n_min + 1, n_min + 20):
    cost = calculate_costs(n_test, rho, lambda_day, alpha)
    if cost < min_cost:
        min_cost = cost
        n_opt = n_test
    else:
        break

print(f"Оптимальное количество каналов (k_opt): {n_opt}")
print(f"Минимальные относительные затраты C(k_opt): {min_cost}")
print()


# 3 Сравнить характеристики обслуживания при kmin и kopt.
print(f"Сравнение характеристик при k_min={n_min} и k_opt={n_opt}")
p0_opt = calculate_p0(rho, n_opt)
l_och_opt = calculate_l_och(rho, n_opt, p0_opt)
l_sist_opt = calculate_l_sist(rho, n_opt, p0_opt)
T_och_opt = l_och_opt / lambda_day
T_sist_opt = l_sist_opt / lambda_day

print(f"{'Характеристика':<25} | {'При n_min':<12} | {'При n_opt':<12}")
print("-" * 55)
print(f"{'Средняя очередь (L_оч)':<25} | {l_och_min:<12.4f} | {l_och_opt:<12.4f}")
print(f"{'Всего в системе (L_сист)':<25} | {l_sist_min:<12.4f} | {l_sist_opt:<12.4f}")
print(f"{'Время ожидания (мин)':<25} | {T_och_min*1440:<12.2f} | {T_och_opt*1440:<12.2f}")
print(f"{'Время в системе (мин)':<25} | {T_sist_min*1440:<12.2f} | {T_sist_opt*1440:<12.2f}")
print()


# 4 Вычислить вероятность того, что в очереди будет находиться не более n
# заявок.

m = 3 

# Расчет для минимального количества каналов (n_min)
p_och_min = calculate_p_och(rho, n_min, p0_min)
prob_queue_min = 1 - p_och_min * ((rho / n_min) ** (m + 1))

# Расчет для оптимального количества каналов (n_opt)
p_och_opt = calculate_p_och(rho, n_opt, p0_opt)
prob_queue_opt = 1 - p_och_opt * ((rho / n_opt) ** (m + 1))

print(f"Вероятность того, что в очереди находится НЕ БОЛЕЕ {m} заявок")
print(f"При минимальном числе каналов (n = {n_min}): P(очередь <= {m}) = {prob_queue_min:.4f}")
print(f"При оптимальном числе каналов (n = {n_opt}): P(очередь <= {m}) = {prob_queue_opt:.4f}")