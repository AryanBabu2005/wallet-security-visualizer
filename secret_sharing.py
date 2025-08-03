import random
from functools import reduce

# Finite field prime (must be > max secret)
PRIME = 208351617316091241234326746312124448251235562226470491514186331217050270460481

def polynom(x, coefficients):
    return sum([c * pow(x, i, PRIME) for i, c in enumerate(coefficients)]) % PRIME

def make_shares(secret, minimum, total):
    if minimum > total:
        raise ValueError("Threshold cannot be more than total shares")

    # random coefficients for polynomial
    coeffs = [secret] + [random.randint(0, PRIME - 1) for _ in range(minimum - 1)]
    shares = [(i, polynom(i, coeffs)) for i in range(1, total + 1)]
    return shares

def reconstruct_secret(shares):
    def _lagrange_basis(j, x):
        numerator, denominator = 1, 1
        for m in range(len(shares)):
            if m != j:
                numerator = (numerator * (-shares[m][0])) % PRIME
                denominator = (denominator * (shares[j][0] - shares[m][0])) % PRIME
        return (shares[j][1] * numerator * pow(denominator, -1, PRIME)) % PRIME

    return sum(_lagrange_basis(j, 0) for j in range(len(shares))) % PRIME
