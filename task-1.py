import formulas

t_obsl = 2.5 # alpha
lambd = 48 # n
k = 6


def solve_1():
    """
        1. Найти минимальное число каналов обслуживания, при котором относительная
        пропускная способность СМО будет не менее 95%.    
    """
    nu = 24 * formulas.nu(t_obsl)
    ro = formulas.ro(lambd, nu)

    n = 1

    while True:
        p0 = formulas.p0(n, ro)
        P_otk = formulas.P_otk(ro, n, p0)
        Q = formulas.Q(P_otk)

        if Q >= 0.95: break

        n += 1

    print(f"Минимальное число каналов обслуживания, при котором относительная пропускная способность СМО будет не менее 95%: {n}")


def solve_2():
    """
        2. Решить задачу для k каналов обслуживания.
    """
    nu = 24 * formulas.nu(t_obsl)
    ro = formulas.ro(lambd, nu)
    p0 = formulas.p0(k, ro)
    P_otk = formulas.P_otk(ro, k, p0)
    Q = formulas.Q(P_otk)
    A = formulas.A(lambd, Q)
    _k = formulas._k(ro, P_otk)

    print("При 6 каналах обслуживания: ")
    print(f"Вероятность отказа (P_отк): {P_otk}")
    print(f"Относительная пропускная способность (Q): {Q}")
    print(f"Абсолютная пропускная способность (A): {A}")
    print(f"Среднее число занятых каналов (¯k): {_k}")
    print(f"Коэффициент загрузки каналов (k_zan): {_k / k}")

def solve_3():
    """
        Определить предельные вероятности состояний системы и основные
        характеристики обслуживания:
            o вероятность отказа;
            o абсолютную и относительную пропускную способность;
            o среднее число занятых каналов;
            o коэффициент загрузки каналов.
    """
    nu = 24 * formulas.nu(t_obsl)
    ro = formulas.ro(lambd, nu)

    print("Предельные вероятности системы:")
    for i in range(0, k + 1):
        P_ = formulas.P_(k, ro, i)
        print(f"Занято {i} канала(ов): {P_}")

# main
solve_1()
print()

solve_2()
print()

solve_3()