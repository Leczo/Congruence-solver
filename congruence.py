from cmath import inf
from collections import defaultdict
import math


def optimize_coefficient(number: int, modulo: int) -> int:
    """
    Function increases or reduces  factors with modulo parameter to obtain positive number close to 0 
    """
    if number < 0:
        number = number + math.ceil(abs(number)/modulo)*modulo
    elif number - modulo > 0:
        number = number - math.floor(number/modulo)*modulo

    return number


def factorization(num: int) -> dict:  #  { number: number of occurences, ...  }
    """
    Returns factors of input number 
    """
    factors: dict = defaultdict(
        int)  # Default dict to simpler calculation
    while num != 1:
        for i in range(2, int(num)+1):
            if num % i == 0:
                num = num / i
                factors[i] += 1
                if num / 1 == 1:
                    return factors
                break
    return factors


def common_divisors(numbers: list) -> list:
    """
    Returns list of common divisors 
    """
    f_array = []
    common = []

    for i in numbers:  # List of decompositions into factors 
        if i == 0:
            return []
        f_array.append(factorization(abs(i)))

    for i in f_array[0]:
        # Adding element if  number is located in every sublist of factors 
        if all(i in f_array[j] for j in range(len(f_array))):
            common.append(i)

    return common


def is_relative_prime(num1: int, num2: int) -> bool:
    """
    Test if pair of numbers contains relative primes numbers
    """
    com_div = common_divisors([num1, num2])
    return True if len(com_div) > 0 else False


def check_relative_primes(a: int, b: int, c: int, d: int, n: int):
    # Error if any pair of numbers is relative prime to modulo factor
    relative_primes = map(lambda x: is_relative_prime(x, n), [a, b, c, d])
    if any(relative_primes):
        print("There is number that is not relative prime to modulo factor")
        print()
        quit()


def least_common_multiple(num1: int, num2: int) -> int:
    """
    Returns lowest common multiple on the base of decomposition to factors 
    """
    if num1 == 0 or num2 == 0:
        return inf

    a_factors = factorization(abs(num1))
    b_factors = factorization(abs(num2))

    factors_merge = [i for i in b_factors.keys(
    ) if i not in a_factors.keys()] + list(a_factors.keys())  # Sum of list containing every occuring divisors 

    lcm = 1
    for num in factors_merge:
        lcm = lcm * num ** max(a_factors[num], b_factors[num])
    return lcm


def greatest_common_divisor(num1: int, num2: int) -> int:
    """
    Returning greatest common divisor  gcd = (num1*num2)/lcm
    """
    lcm = least_common_multiple(num1, num2)
    gcd = (num1*num2)/lcm
    return int(gcd)


def reduce_one_coefficient(a: int, b: int, c: int, d: int, e: int, f: int, n: int,  lcm: int, var: str) -> tuple:
    """
    Reducing one coefficient to simplify equation
    Returns factor on the left side of equation and value on its right side
    """
    if var == "x":
        num1 = a
        num2 = c
    else:
        num1 = b
        num2 = d

    quotient1 = abs(int(lcm/num1))
    quotient2 = abs(int(lcm/num2))

    # If both numbers have the same sign multiply to reduce -1 
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

    left_s = a+b+c+d  #sum of number on the left side of equation a and c or b and d are going to be reduce 
    right_s = e+f  # sum of numbers on the right side of equation 

    print(
        f"Adding first equation multiplied by {quotient1} and the second one by {quotient2}")
    print("----------------------------------------------------------")
    print("Transformed equation", "\n")
    print(f"{a}x + {b}y ≡{n} {e} ")
    print(f"{c}x + {d}y ≡{n} {f} ")
    print()
    return left_s, right_s


def possible_solutions(num1: int, num2: int, modulo: int):
    """
    Return number of possible solutions of congruence 
    Equation have solution if gdc(num1, modulo)
    """
    p_solutions = greatest_common_divisor(num1, modulo)

    if (num2 % p_solutions) != 0:
        print("----------------------------------------------------------")
        print("No solutions")
        quit()
    else:
        print(f"Number of solutions: {p_solutions}")
        print("----------------------------------------------------------")
        print()


def solve_congruence(num1: int, num2: int, modulo: int, constant=None) -> int:
    """
    Return congruence result
    """

    num1 = optimize_coefficient(num1, modulo)
    num2 = optimize_coefficient(num2, modulo)

    if not constant:  # if without constant 
        possible_solutions(num1, num2, modulo)

        # While loop to the moment of achievement of 1*variable on the left side of equation or 0 on the rifht side 
        while num1 != 1 and num2 != 0:
            cd = common_divisors([num1, num2])

            # If lacking common divisors we are adding modulo to number on the right side 
            if len(cd) == 0:
                num2 += modulo
                continue

            # Splitting two numbers by their highest common divisor
            max_cd = max(cd)
            num1 = int(num1/max_cd)
            num2 = int(num2/max_cd)
        return num2

    if constant:
        constant = constant * -1  # *-1 because we are swapping on the right side of equation 
        flag = 0  # to alternate addition of modulo to constant and number on the right side 
        constant = optimize_coefficient(constant, modulo)
        while num1 != 1 and (num2 != 0 and constant != 0):
            cd = common_divisors([num1, num2, constant])

            # If lacking common divisors we are adding modulo to factor next to constant or value on the right side 
            if len(cd) == 0:

                if flag == 0:
                    num2 += modulo
                    flag += 1
                    continue

                if flag == 1:
                    constant += modulo
                    flag -= 1
                    continue

            # Splitting two numbers by their highest common divisor
            max_cd = max(cd)
            num1 = int(num1/max_cd)
            num2 = int(num2/max_cd)
            constant = int(constant/max_cd)
        return optimize_coefficient(num2, modulo), optimize_coefficient(constant, modulo)


def solve(a: int, b: int, c: int, d: int, e: int, f: int, n: int) -> tuple:

    check_relative_primes(a, b, c, d, n)
    # Coefficients optimalization
    a = optimize_coefficient(a, n)
    b = optimize_coefficient(b, n)
    c = optimize_coefficient(c, n)
    d = optimize_coefficient(d, n)
    e = optimize_coefficient(e, n)
    f = optimize_coefficient(f, n)

    print("Optimal coefficients")
    print("----------------------------------------------------------")
    print(f"{a}x + {b}y ≡{n} {e} ")
    print(f"{c}x + {d}y ≡{n} {f} ")
    print()

    not_zero = [i for i in [a, b, c, d, e, f] if i != 0]
    if len(not_zero) == 2:
        value = solve_congruence(not_zero[0], not_zero[1], n)
        print("Result")
        print("=====================")
        print(f"x ≡{n} {value}")
        print("=====================", '\n')
        quit()

    # Case one equation with two unknowns
    if (a == 0 and b == 0) or (c == 0 and d == 0):
        if a == 0 and b == 0:  # jeżeli brak wartości ax + by podstawiamy c i d pod b w celu wykonania obliczeń wyłącznie na pierwszym równaniu
            a, b = c, d
        # a is factor next to constant because we operate on single equation
        value = solve_congruence(b, e, n, a)
        print("Result")
        print("=====================")
        print(f"x ≡{n} c")
        print(f"y ≡{n} {value[1]}c + {value[0]}")
        print("=====================", '\n')
        quit()

    # Case, two equations where every contains only one unknown
    if (a == 0 and d == 0) or (c == 0 and b == 0):
        if a == 0 and d == 0:
            y_coef, y_right_side = b, e
            x_coef, x_right_side = c, f
        elif b == 0 and c == 0:
            x_coef, x_right_side = a, e
            y_coef, y_right_side = d, f
            c = a

        print("X - ", end="")
        x_value = solve_congruence(x_coef, x_right_side, n)
        print("Y - ", end="")
        # x value substitution
        y_value = solve_congruence(y_coef, y_right_side, n)

    # Case, two equations two unknows
    else:
        # Lowest common multiple for both variables
        x_lcm = (least_common_multiple(a, c), "x")
        y_lcm = (least_common_multiple(b, d), "y")

        lcm, variable = min(x_lcm, y_lcm, key=lambda x: x[0])

        print(f"Variable reduction {variable}")
        left_side, right_side = reduce_one_coefficient(
            a, b, c, d, e, f, n, lcm, variable)

        # If equations reduces itself we are adding constant to equation
        if left_side == 0:
            value = solve_congruence(b, e, n, a)
            print("Result")
            print("=====================")
            print(f"x ≡{n} c")
            print(f"y ≡{n} {value[1]}c + {value[0]}")
            print("=====================", '\n')
            quit()

        if variable == "y":
            print("X - ", end="")
            x_value = solve_congruence(left_side, right_side, n)
            # Value substitution x under {𝑎𝑥 + 𝑏𝑦 ≡𝑛 c
            print("Y - ", end="")
            y_value = solve_congruence(b, e - a*x_value, n)

        if variable == "x":
            print("Y - ", end="")
            y_value = solve_congruence(left_side, right_side, n)
            # Value substitution y under {𝑎𝑥 + 𝑏𝑦 ≡𝑛 c
            print("X - ", end="")
            x_value = solve_congruence(a, e-b*y_value, n,)

    print("Result")
    print("=====================")
    print(f"x ≡{n} {x_value}")
    print(f"y ≡{n} {y_value}")
    print("=====================", '\n')


def main(a, b, c, d, e, f, n):
    """
        Equation type:
        {𝑎𝑥 + 𝑏𝑦 ≡𝑛 c
        {d𝑥 + e𝑦 ≡𝑛 𝑓

    """
    print("Equation")
    print("----------------------------------------------------------")
    print(f"{a}x + {b}y ≡{n} {e} ")
    print(f"{c}x + {d}y ≡{n} {f} ")
    print()
    solve(a, b, c, d, e, f, n)


if __name__ == "__main__":
    # main(a, b, c, d, e, f, n)
    # Example equation:
    #{ 4x + -7y ≡37 19 
    #{ 1x + 8y ≡37 18 
    main(4,-7,19,1,8,18,37)
