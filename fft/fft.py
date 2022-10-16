import math


class oldNumber:
    def __init__(
        self,
        basic=True,
        base=None,
        complexA=None,
        complexB=None,
        complexC=None,
    ):
        self.basic = basic
        if basic:
            self.base = base
            self.theta = 0
            self.r = base
        else:
            # We want this to equal A + B * C
            # Essentially, we will add some values together and not others

            self.complexA = complexA
            self.complexB = complexB
            self.complexC = complexC


class Number:
    def __init__(self, r, theta):
        self.r = r
        self.theta = theta

    def __repr__(self):
        return f"({self.r}, {self.theta})"


def combine(a, b, c):
    first = a
    second = num_mult(b, c)
    # Add the two together

    x1 = first.r * math.cos(first.theta)
    x2 = second.r * math.cos(second.theta)
    y1 = first.r * math.sin(first.theta)
    y2 = second.r * math.sin(second.theta)

    new_r = math.sqrt(math.pow(x1 + x2, 2) + math.pow(y1 + y2, 2))
    new_theta = math.atan2(y1 + y2, x1 + x2)
    return Number(new_r, new_theta)


def num_mult(a, b):
    return Number(a.r * b.r, a.theta + b.theta)
    # if a.theta == 0:
    #     return Number(a.r * b.r, b.theta)
    # if b.theta == 0:
    #     return Number(a.r * b.r, a.theta)
    # # Both are complex, perform special math
    # x1 = a.r * math.cos(a.theta)
    # x2 = b.r * math.cos(b.theta)
    # y1 = a.r * math.sin(a.theta)
    # y2 = b.r * math.sin(b.theta)

    # new_r = math.sqrt(math.pow(x1 * x2 - y1 * y2, 2) + math.pow(x1 * y2 + x2 * y1, 2))
    # new_theta = math.atan2((x1 * y2 + x2 * y1) / (x1 * x2 - y1 * y2))
    # return Number(new_r, new_theta)


def multiply(a, b):
    # How to multiply:
    # 1 - convert numbers into polynomial form (expand size to n)
    # 2 - convert numbers into point-value form
    # 3 - multiply point-value form polynomials
    # 4 - convert back into polynomial form
    # 5 - convert into a number

    # 1 - convert numbers into polynomial form (expand size to n)
    n = math.ceil(math.log(a, 2)) + math.ceil(math.log(b, 2)) + 2
    # Round n up to a power of 2
    n = 1 << math.ceil(math.log(n, 2))
    print(f"BASE: n={n}")
    poly_a = num_to_poly(a, n)
    poly_b = num_to_poly(b, n)

    print(f"poly_a: {poly_a}, poly_b: {poly_b}")
    # 2 - convert numbers into point-value form
    # use FFT to do this?????????
    x = Number(1, 2 * math.pi / n)
    pv_a = poly_to_pv([Number(num, 0) for num in poly_a], n, x)
    pv_b = poly_to_pv([Number(num, 0) for num in poly_b], n, x)

    # 3 - multiply point-value form polynomials
    pv_product = multiply_pv(pv_a, pv_b, n)

    # 4 - convert back into polynomial form
    poly_product = pv_to_poly(pv_product, n, x)

    # 5 - convert into a number
    product = poly_to_num(poly_product, n)

    return product


def num_to_poly(num, n):
    return [(num >> i) & 1 for i in range(n)]


def poly_to_pv(poly_num, n, x):
    if n == 1:
        return [poly_num[0]]

    poly_even = [poly_num[i] for i in range(0, n, 2)]
    poly_odd = [poly_num[i] for i in range(1, n, 2)]
    print(n)
    print(f"poly_num: {poly_num}")
    print(f"poly_even: {poly_even}")
    print(f"poly_odd: {poly_odd}")
    pv_even = poly_to_pv(poly_even, int(n / 2), num_mult(x, x))
    pv_odd = poly_to_pv(poly_odd, int(n / 2), num_mult(x, x))

    print(n)
    print(f"poly_num: {poly_num}")
    print(f"poly_even: {poly_even}")
    print(f"poly_odd: {poly_odd}")
    print(f"pv_even: {pv_even}")
    print(f"pv_odd: {pv_odd}")

    pv_num = [None] * n
    for k in range(int(n / 2)):
        pv_num[k] = combine(pv_even[k], x, pv_odd[k])
        x.r = -x.r
        pv_num[k + int(n / 2)] = combine(pv_even[k], x, pv_odd[k])
        x.r = -x.r

    print(f"Made {pv_num} from x: {x}")

    return pv_num


def multiply_pv(pv_a, pv_b, n):
    return [num_mult(pv_a[i], pv_b[i]) for i in range(n)]


def pv_to_poly(pv_num, n, x):
    # invert x
    x.r = -x.r
    poly_out = poly_to_pv(pv_num, n, x)
    x.r = -x.r
    return [Number(num.r / n, num.theta) for num in poly_out]


def poly_to_num(num, n):
    print(f"Running poly_to_num on {num}")
    sum = [0, 0]
    for i in range(n):
        num[i].r *= 2 << n
        sum[0] += num[i].r * math.cos(num[i].theta)
        sum[1] += num[i].r * math.sin(num[i].theta)
    return sum
