from collections import defaultdict
import math


def optimize_coefficient(number: int, modulo: int) -> int:
    if number < 0:
        number = number + math.ceil(abs(number)/modulo)*modulo
    elif number - modulo > 0:
        number = number - math.floor(number/modulo)*modulo

    return number


def is_relative_prime(num1: int, num2: int) -> bool:
    com_div = common_divisors(num1, num2)
    return True if len(com_div) > 0 else False


def factorization(num: int) -> dict:  # { number: count, ...}
    factors: dict = defaultdict(int)  # default value of item is 0
    while num != 1:
        for i in range(2, int(num)+1):
            if num % i == 0:
                num = num / i
                factors[i] += 1
                if num / 1 == 1:
                    return factors
                break
    return factors


def common_divisors(num1: int, num2: int) -> list:
    a_factors = factorization(abs(num1))
    b_factors = factorization(abs(num2))
    return [i for i in a_factors.keys() if i in b_factors.keys()]


def greatest_common_divisor(num1: int, num2: int) -> int:
    lcm = least_common_multiple(num1, num2)
    gcd = (num1*num2)/lcm
    return int(gcd)


def least_common_multiple(num1: int, num2: int) -> int:
    a_factors = factorization(abs(num1))
    b_factors = factorization(abs(num2))

    factors_merge = [i for i in b_factors.keys(
    ) if i not in a_factors.keys()] + list(a_factors.keys())

    lcm = 1
    for num in factors_merge:
        lcm = lcm * num ** max(a_factors[num], b_factors[num])
    return lcm


def reduce_one_coefficient(num1: int, num2: int, a: int, b: int, c: int, d: int, e: int, f: int, n: int,  lcm: int) -> tuple:
    quotient1 = abs(int(lcm/num1))
    quotient2 = abs(int(lcm/num2))

    # if both numbers have same sign *-1 to reduce them
    if (num1 > 0 and num2 > 0) or (num1 < 0 and num2 < 0):
        a *= -1
        b *= -1
        e *= -1

    a *= quotient1
    b *= quotient1
    e *= quotient1

    c *= quotient2
    d *= quotient2
    f *= quotient2

    # (y or x) * coefficient variable depending of conditional statement
    variable = a+b+c+d
    number = e+f  # sum of numbers after equal sign in equation
    print(
        f"Adding first equation multiplied by {quotient1} and second by {quotient2}")
    print("----------------------------------------------------------")
    print(f"{a}x + {b}y ≡{n} {e} ")
    print(f"{c}x + {d}y ≡{n} {f} ")
    print()
    return variable, number


def possible_solutions(num1: int, num2: int, modulo: int):
    p_solutions = greatest_common_divisor(num1, modulo)
    if (num2 % p_solutions) != 0:
        print("----------------------------------------------------------")
        print("No Solutions")
        quit()
    else:
        print(f"Solutions: {p_solutions}")
        print("----------------------------------------------------------")
        print()


def solve_congruence(num1: int, num2: int, modulo: int) -> int:
    num1 = optimize_coefficient(num1, modulo)
    num2 = optimize_coefficient(num2, modulo)

    possible_solutions(num1, num2, modulo)

    while num1 != 1 and num2 != 0:
        cd = common_divisors(num1, num2)

        if len(cd) == 0:
            num2 += modulo
            continue

        max_cd = max(cd)
        num1 = int(num1/max_cd)
        num2 = int(num2/max_cd)
    return num2


def solve(a: int, b: int, c: int, d: int, e: int, f: int, n: int) -> tuple:

    # Error if any number is not relative prime number
    relative_primes = map(lambda x: is_relative_prime(x, n), [a, b, c, d])
    if any(relative_primes):
        print("There is none relative prime number")
        print(list(relative_primes))
        print("")
        quit()

    # Optimising coefficients to remove negative numbers
    a = optimize_coefficient(a, n)
    b = optimize_coefficient(b, n)
    c = optimize_coefficient(c, n)
    d = optimize_coefficient(d, n)
    e = optimize_coefficient(e, n)
    f = optimize_coefficient(f, n)

    print("Optimized coefficients")
    print("----------------------------------------------------------")
    print(f"{a}x + {b}y ≡{n} {e} ")
    print(f"{c}x + {d}y ≡{n} {f} ")
    print()
    x_lcm = least_common_multiple(a, c)
    y_lcm = least_common_multiple(b, e)

    if x_lcm < y_lcm:
        print("Reducing variable x")
        variable, number = reduce_one_coefficient(
            a, c, a, b, c, d, e, f, n, x_lcm)

        y_value = solve_congruence(variable, number, n)

        print("Simplified equations")
        print("----------------------------------------------------------")
        print(f"{variable}x ≡{n} {number}")
        print(f"{a*y_value+b}y ≡{n} {e}", 2*"\n")
        # Substituting y value in  {𝑎𝑥 + 𝑏𝑦 ≡𝑛 e
        x_value = solve_congruence(a, e-b*y_value, n)

    else:
        print("Reducing variable y")
        variable, number = reduce_one_coefficient(
            b, d, a, b, c, d, e, f, n, y_lcm)

        x_value = solve_congruence(variable, number, n)

        print("Simplified equations")
        print("----------------------------------------------------------")
        print(f"{variable}x ≡{n} {number}")
        print(f"{a*x_value+b}y ≡{n} {e}", 2*"\n")
        # Substituting x value in  {𝑎𝑥 + 𝑏𝑦 ≡𝑛 e
        y_value = solve_congruence(b, e - a*x_value, n)

    print()
    print("Result")
    print("=====================")
    print(f"x ≡{n} {x_value}")
    print(f"y ≡{n} {y_value}")
    print("=====================", '\n')


def main(a, b, c, d, e, f, n):
    """
        Equation Template:
        {𝑎𝑥 + 𝑏𝑦 ≡𝑛 e
        {c𝑥 + d𝑦 ≡𝑛 𝑓

    """
    print("Equation")
    print("----------------------------------------------------------")
    print(f"{a}x + {b}y ≡{n} {e} ")
    print(f"{c}x + {d}y ≡{n} {f} ")
    print()

    solve(a, b, c, d, e, f, n)


if __name__ == "__main__":

    #main(a, b, c, d, e, f, n)
    #Example  function values 
    main(5, -2, -2, 4, 4, -3, 11)  # a=5, b=(-2)...