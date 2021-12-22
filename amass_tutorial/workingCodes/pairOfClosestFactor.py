## https://gist.github.com/iansan5653/1e306da9688d85934385b266e74f153a
def calc_closest_factors(c: int):
    """Calculate the closest two factors of c.

    Returns:
      [int, int]: The two factors of c that are closest; in other words, the
        closest two integers for which a*b=c. If c is a perfect square, the
        result will be [sqrt(c), sqrt(c)]; if c is a prime number, the result
        will be [1, c]. The first number will always be the smallest, if they
        are not equal.
    """
    if c // 1 != c:
        raise TypeError("c must be an integer.")

    a, b, i = 1, c, 0
    while a < b:
        i += 1
        if c % i == 0:
            a = i
            b = c // a

    return [b, a]

# rows, cols = calc_closest_factors(24)
# print(rows, cols)