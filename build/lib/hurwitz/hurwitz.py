from math import floor, ceil
from functools import reduce
import warnings

class HurwitzQuaternion:
    def __init__(self, a: int, b: int, c: int, d: int, half: bool = False) -> None:
        if not all(isinstance(val, int) for val in [a, b, c, d]):
            raise TypeError("All values must be ints")
        if half:
            # check to see if a b c or d is divisible by 2
            if a % 2 == 0 or b % 2 == 0 or c % 2 == 0 or d % 2 == 0:
                # if all are divisible by 2, then it is a whole quaternion.
                if a % 2 == 0 and b % 2 == 0 and c % 2 == 0 and d % 2 == 0:
                    half = False
                    a = a // 2
                    b = b // 2
                    c = c // 2
                    d = d // 2
                else:
                    raise ValueError("Half quaternions must not have individual values divisible by 2")
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        # ±1, ±i, ±j, ±k, 
        self.unitary_whole_quaternions = {
            (1, 0, 0, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, -1, 0, 0),
            (0, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, 1), (0, 0, 0, -1)
        }
        # (±1 ± i ± j ± k)/2
        self.unitary_half_quaternions = {
            (1, 1, 1, 1), (-1, -1, -1, -1), (1, -1, 1, -1), (-1, 1, -1, 1), (1, 1, -1, -1), (-1, -1, 1, 1),
            (1, -1, -1, 1), (-1, 1, 1, -1), (1, 1, 1, -1), (-1, -1, -1, 1), (1, 1, -1, 1), (-1, -1, 1, -1),
            (1, -1, 1, 1), (-1, 1, -1, -1), (1, -1, -1, -1), (-1, 1, 1, 1)
        }
        self.half = half
        self.trace = 2*a if self.half == False else a
        self.general = (a, b, c, d) if self.half == False else (a/2, b/2, c/2, d/2)

    def __add__(self, other: 'HurwitzQuaternion') -> 'HurwitzQuaternion':
        if not isinstance(other, HurwitzQuaternion):
            raise TypeError("Can only add HurwitzQuaternion to HurwitzQuaternion")
        if self.half == other.half == False:
            return HurwitzQuaternion(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d, False)
        elif self.half == other.half == True:
            return HurwitzQuaternion((self.a + other.a) // 2, (self.b + other.b) // 2, (self.c + other.c) // 2, (self.d + other.d) // 2, False)
        else:
            if self.half:
                return HurwitzQuaternion(self.a + 2 * other.a, self.b + 2 * other.b, self.c + 2 * other.c, self.d + 2 * other.d, True)
            else:
                return HurwitzQuaternion(2 * self.a + other.a, 2 * self.b + other.b, 2 * self.c + other.c, 2 * self.d + other.d, True)

    def __sub__(self, other: 'HurwitzQuaternion') -> 'HurwitzQuaternion':
        if not isinstance(other, HurwitzQuaternion):
            raise TypeError("Can only subtract HurwitzQuaternion from HurwitzQuaternion")
        # Multiply the other quaternion by -1 and add
        return self + HurwitzQuaternion(-other.a, -other.b, -other.c, -other.d, other.half)

    def __mul__(self, other) -> 'HurwitzQuaternion':
        if isinstance(other, HurwitzQuaternion):
            if self.half == other.half:
                return HurwitzQuaternion(
                    self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d,
                    self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c,
                    self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b,
                    self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a,
                    self.half
                )
            else:
                # If one is half and the other is not, convert half to whole for the operation
                if self.half:
                    factor = 2
                else:
                    factor = 1
                results = [
                    factor * (self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d),
                    factor * (self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c),
                    factor * (self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b),
                    factor * (self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a)]
                if results[0] % 2 == 0 and results[1] % 2 == 0 and results[2] % 2 == 0 and results[3] % 2 == 0:
                    return HurwitzQuaternion(results[0] // 2, results[1] // 2, results[2] // 2, results[3] // 2, False)
                else:
                    return HurwitzQuaternion(results[0], results[1], results[2], results[3], True)
        elif isinstance(other, int):
            if (other % 2 == 0) and self.half == True:
                return HurwitzQuaternion(
                    int(self.a * other // 2),
                    int(self.b * other // 2),
                    int(self.c * other // 2),
                    int(self.d * other // 2),
                    False
                )
            else:
                return HurwitzQuaternion(
                    int(self.a * other),
                    int(self.b * other),
                    int(self.c * other),
                    int(self.d * other),
                    self.half
                )
        else:
            warnings.warn("Multiplying HurwitzQuaternion by a non-int will result in a tuple of quaternion vals, not a Hurwitz Quaternion")
            if self.half:
                return (self.a * other, self.b * other, self.c * other, self.d * other)
            else:
                return (self.a * other * 2, self.b * other * 2, self.c * other * 2, self.d * other * 2)

    def __neg__(self) -> 'HurwitzQuaternion':
        return HurwitzQuaternion(-self.a, -self.b, -self.c, -self.d, self.half)

    def __repr__(self) -> str:
        return f"{self.a} + {self.b}i + {self.c}j + {self.d}ij" if self.half == False else f"{self.a}/2 + {self.b}/2i + {self.c}/2j + {self.d}/2ij"

    def __len__(self) -> float:
        return self.norm()

    def __getitem__(self, key: int) -> float:
        if self.half:
            return [self.a, self.b, self.c, self.d][key] / 2
        else:
            return [self.a, self.b, self.c, self.d][key]

    def __eq__(self, other: 'HurwitzQuaternion') -> bool:
        if not isinstance(other, HurwitzQuaternion):
            return False
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d

    def __hash__(self) -> int:
        return hash((self.a, self.b, self.c, self.d))

    def __floordiv__(self, other: 'HurwitzQuaternion') -> 'HurwitzQuaternion':
        return self.euclidean_division(other)[0]

    def __truediv__(self, other: 'HurwitzQuaternion') -> 'HurwitzQuaternion':
        # warn that this doesnt return a hurwitz quaternion
        warnings.warn("True Division of HurwitzQuaternion by another HurwitzQuaternion will return a tuple of quaternion values, not a Hurwitz Quaternion")
        return self.general_quaternion_division(self, other)

    def __mod__(self, other: 'HurwitzQuaternion') -> 'HurwitzQuaternion':
        return self.euclidean_division(other)[1]
    
    def norm(self) -> float:
        if self.half == False:
            return (self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2)**0.5
        else:
            return ((self.a/2) ** 2 + (self.b/2) ** 2 + (self.c/2) ** 2 + (self.d/2) ** 2)**0.5

    def conjugate(self) -> 'HurwitzQuaternion':
        return HurwitzQuaternion(self.a, -self.b, -self.c, -self.d, self.half)

    def unitary(self) -> bool:
        # Q is invertible if ∃q ∈ A such that qq' = q'q = 1.
        # can be calculated with `self.norm() == 1`, but a hash table is faster since there are only 24 cases

        # Check if the current quaternion is in the appropriate set
        if self.half:
            return (self.a, self.b, self.c, self.d) in self.unitary_half_quaternions
        else:
            return (self.a, self.b, self.c, self.d) in self.unitary_whole_quaternions

    def invertable(self) -> bool:
        # Q is invertible if ∃q ∈ A such that qq' = q'q, and that qq' ∈ A. this only is true if the HQ is unitary
        return self.unitary()
        
    def inverse(self) -> 'HurwitzQuaternion':
        # Define a dictionary mapping each unitary quaternion to its inverse
        unitary_inverses = {
            (1, 0, 0, 0): (1, 0, 0, 0), (-1, 0, 0, 0): (-1, 0, 0, 0), (0, 1, 0, 0): (0, -1, 0, 0),
            (0, -1, 0, 0): (0, 1, 0, 0), (0, 0, 1, 0): (0, 0, -1, 0), (0, 0, -1, 0): (0, 0, 1, 0),
            (0, 0, 0, 1): (0, 0, 0, -1), (0, 0, 0, -1): (0, 0, 0, 1), (1, 1, 1, 1): (1, -1, -1, -1),
            (-1, -1, -1, -1): (-1, 1, 1, 1), (1, -1, 1, -1): (1, 1, -1, 1), (-1, 1, -1, 1): (-1, -1, 1, -1),
            (1, 1, -1, -1): (1, -1, 1, 1), (-1, -1, 1, 1): (-1, 1, -1, -1), (1, -1, -1, 1): (1, 1, 1, -1),
            (-1, 1, 1, -1): (-1, -1, -1, 1), (1, 1, 1, -1): (1, -1, -1, 1), (-1, -1, -1, 1): (-1, 1, 1, -1),
            (1, 1, -1, 1): (1, -1, 1, -1), (-1, -1, 1, -1): (-1, 1, -1, 1), (1, -1, 1, 1): (1, 1, -1, -1),
            (-1, 1, -1, -1): (-1, -1, 1, 1), (1, -1, -1, -1): (1, 1, 1, 1), (-1, 1, 1, 1): (-1, -1, -1, -1)
        }

        # Get the quaternion tuple
        quaternion = (self.a, self.b, self.c, self.d)

        # Return the inverse if the quaternion is unitary, otherwise raise an exception
        if quaternion in unitary_inverses:
            inv = unitary_inverses[quaternion]
            return HurwitzQuaternion(inv[0], inv[1], inv[2], inv[3], self.half)
        else:
            raise ValueError("The quaternion is not unitary and therefore does not have an inverse in 𝐴.")

    def general_inverse(self) -> tuple:
        # Defined for non-unitary quaternions, returns the inverse as a tuple
        conjugate = self.conjugate()
        values = conjugate.general
        norm = self.norm() ** 2
        print("Conjugate:", repr(conjugate))
        print("Conjugate Values:", values)
        print("Norm:", norm)
        ginv = tuple([val / norm for val in values])
        print("General Inverse:",ginv )
        return ginv

    @staticmethod
    def factors(n):
        # Credit to https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
        return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

    @staticmethod
    def general_norm(a: tuple) -> float:
        return (a[0] ** 2 + a[1] ** 2 + a[2] ** 2 + a[3] ** 2)**0.5

    def euclidean_division(self, other: 'HurwitzQuaternion') -> ('HurwitzQuaternion', 'HurwitzQuaternion'):
        # source: https://m-hikari.com/imf/imf-2012/41-44-2012/perngIMF41-44-2012.pdf
        if not isinstance(other, HurwitzQuaternion):
            raise TypeError("Can only divide by another HurwitzQuaternion")
        if other.a == other.b == other.c == other.d == 0:
            raise ZeroDivisionError("Cannot divide by zero quaternion")

        print("Attempting to divide a:", repr(self), "by b:", repr(other))
        # Calculate general inverse of the divisor b^-1
        binv = other.general_inverse()
        print("Inverse of divisor: b^-1", binv)
        # Calculate general product of the dividend and the divisor inverse: a*b^-1
        abinv = self.general_quaternion_multiplication(self.general, binv)
        print("General product of dividend and inverse: ab^-1", abinv)
        # Round the coefficients of the general product to the nearest integer, givning a number q which has 
        # coefficients which are 1/2 or less away from the coefficients of the general product
        # q : abs(n_i) ≤ 1/2 ∀ n_i ∈ n_1 + n_2*i + n_3*j + n_3*k = a*(b^-1) - q
        q_whole = [round(val) for val in abinv]
        # try rounding every number to a half int, NOT a whole int
        q_half = [self.round_to_only_half(val) for val in abinv]


        print("Int Rounded general product: q=", q_whole)
        print("Half Rounded general product: q=", q_half)
        qb_whole = self.general_quaternion_multiplication(other.general, q_whole)
        gb_whole_norm = self.general_norm([qb_whole[i] - self.general[i] for i in range(4)])
        print(f"Product of divisor and whole rounded product: qb={qb_whole} with norm {gb_whole_norm}")
        qb_half = self.general_quaternion_multiplication(other.general, q_half)
        gb_half_norm = self.general_norm([qb_half[i] - self.general[i] for i in range(4)])
        print(f"Product of divisor and half rounded product: qb={qb_half} with norm {gb_half_norm}")
        delta_half = abs(self.norm() - gb_whole_norm)
        delta_whole = abs(self.norm() - gb_half_norm)
        print("Delta Whole:", delta_whole)
        print("Delta Half:", delta_half)
        if delta_half < delta_whole:
            q = q_half
        else:
            q = q_whole

        print(f"Resultant formula: a = qb + r -> {repr(self)} = ({repr(other)})({q[0]} + {q[1]}i + {q[2]}j + {q[3]}ij) + r")
        # calculate qb
        qb = self.general_quaternion_multiplication(other.general, q)
        print("Product of divisor and rounded product: qb=", qb)

        # Calculate the error between the rounded product and the general product
        r = [self.general[i] - qb[i] for i in range(4)]
        print("Difference between rounded product and general product: r = ", r)
        r_rounded_to_half = [self.round_to_nearest_half(val) for val in r]
        r_preprocess = [int(r_rounded_to_half[i]*2) for i in range(4)]
        q_rounded_to_half = [self.round_to_nearest_half(val) for val in q]   
        q_preprocess = [int(q_rounded_to_half[i]*2) for i in range(4)]
        print("Rounded/doubled preprocesed r:", r_preprocess)
        print("Rounded/doubled preprocesed q:", q_preprocess)
        return (HurwitzQuaternion(*q_preprocess, True), HurwitzQuaternion(*r_preprocess, True))

    def euclidean_division_pro_max(self, other: 'HurwitzQuaternion') -> ('HurwitzQuaternion', 'HurwitzQuaternion'):
        # like regular euclidean division, but also tries to divide the conjuigate of the dividend by the divisor
        # and returns the result with the smallest remainder
        forward = self.euclidean_division(other)
        backward = self.conjugate().euclidean_division(other)
        if forward[1].norm() > backward[1].norm():
            print("Conjugate division has smaller remainder by ", forward[1].norm() - backward[1].norm())
            return backward
        elif forward[1].norm() < backward[1].norm():
            print("Regular division has smaller remainder by ", backward[1].norm()- forward[1].norm())
            return forward
        else:
            print("Remainders are equal, returning regular division")
            return forward

    def snap(self, general_quaternion: tuple) -> 'HurwitzQuaternion':
        # Round the values of the general quaternion to the nearest integer or half
        g_norm = self.general_norm(general_quaternion)

        g_whole = [round(val) for val in general_quaternion]
        g_half = [self.round_to_only_half(val) for val in general_quaternion]

        g_whole_norm = self.general_norm(g_whole)
        g_half_norm = self.general_norm(g_half)

        delta_half = abs(g_norm - g_whole_norm)
        delta_whole = abs(g_norm - g_half_norm)
        g = []
        if delta_half < delta_whole:
            g = g_half
        else:
            g = g_whole
        
        g_rounded_to_half = [self.round_to_nearest_half(val) for val in g]   
        g_preprocess = [int(g_rounded_to_half[i]*2) for i in range(4)]

        return HurwitzQuaternion(*g_preprocess, True)

    def decompose(self) -> list:
        q_b, r_b = self.euclidean_division(HurwitzQuaternion(1, 1, 1, 1, True))
        print("Decomposition of", repr(self))
        general = self.general
        if self.half:
            r_h = (general[0]/abs(general[0]))*0.5
            i_h = (general[1]/abs(general[1]))*0.5
            j_h = (general[2]/abs(general[2]))*0.5
            k_h = (general[3]/abs(general[3]))*0.5
        else:
            r_h = 0
            i_h = 0
            j_h = 0
            k_h = 0

        r = general[0] - r_h
        i = general[1] - i_h
        j = general[2] - j_h
        k = general[3] - k_h
        print("General whole quat:", r, i, j, k)
        # return n unitary quaternion for each value in self
        real = [HurwitzQuaternion(int(r/abs(r)), 0, 0, 0) for _ in range(int(abs(r)))]
        imag = [HurwitzQuaternion(0, int(i/abs(i)), 0, 0) for _ in range(int(abs(i)))]
        jmag = [HurwitzQuaternion(0, 0, int(j/abs(j)), 0) for _ in range(int(abs(j)))]
        kmag = [HurwitzQuaternion(0, 0, 0, int(k/abs(k))) for _ in range(int(abs(k)))]
        whole_part = real + imag + jmag + kmag
        
        if self.half == False:
            return whole_part
        else:
            half_unit = HurwitzQuaternion(int(r_h*2), int(i_h*2), int(j_h*2), int(k_h*2), True)
            print("Half part unit quat:", repr(half_unit))
            return whole_part + [half_unit]

    def imaginary_string(self) -> str:
        stringReps = []
        suffix = extra = ""
        if self.half:
            suffix = "/2"
            extra = "1/2"

        def unit_symbol(val, symbol, symbol_alt):
            if val == 0:
                return None
            if val == 1:
                return extra + symbol
            if val == -1:
                return extra + symbol_alt
            if val > 0:
                return f"{val}{suffix}{symbol}"
            if val < 0 and symbol_alt:
                return f"{val}{suffix}{symbol_alt}"
            return None

        symbols = [
            unit_symbol(self.a, "1", "-1"),
            unit_symbol(self.b, "i", "-i"),
            unit_symbol(self.c, "j", "-j"),
            unit_symbol(self.d, "k", "-k")
        ]

        for symbol in symbols:
            if symbol:
                stringReps.append(symbol)

        return " + ".join(stringReps)

    def __str__(self) -> str:
        return self.imaginary_string()

    def symbolic_rep(self) -> str:
        stringReps = []
        suffix = extra = ""
        if self.half:
            suffix = "/2"
            extra = "1/2 x "

        def unit_symbol(val, symbol, symbol_alt):
            if val == 0:
                return None
            if val == 1:
                return extra + symbol
            if val == -1:
                return extra + symbol_alt
            if val > 0:
                return f"{val}{suffix} x {symbol}"
            if val < 0 and symbol_alt:
                return f"{val}{suffix} x {symbol_alt}"
            return None

        symbols = [
            unit_symbol(self.a, "↔", None),
            unit_symbol(self.b, "→", "←"),
            unit_symbol(self.c, "∋", "∈"),
            unit_symbol(self.d, "⊂", "⊃")
        ]

        for symbol in symbols:
            if symbol:
                stringReps.append(symbol)

        return " + ".join(stringReps)

    def verbose_string(self) -> str:
        return f"{self.a} + {self.b}i + {self.c}j + {self.d}ij"

    def associates(self):
        # get all associates of the quaternion
        associates = [] 
        # multiply by all unitary quaternions
        for unitary in self.unitary_whole_quaternions:
            associates.append(HurwitzQuaternion(*unitary)*self)
        for unitary in self.unitary_half_quaternions:
            associates.append(HurwitzQuaternion(*unitary, True)*self)
        return associates

    def equivalence_class(self):
        # get the equivalence class of the quaternion
        return self.conjugate().associates() + self.associates()

    def association_check(self, q1, q2) -> bool:
        """
        Check if two quaternions are associates.
        """
        if q1.norm() == q2.norm():
            q1_associates = q1.associates()
            print(q1_associates)
            print(q2.general)
            if q2 in q1_associates:
                return True
        return False

    @staticmethod
    def round_to_nearest_half(x):
        return floor(x) if x - floor(x) < 0.25 else ceil(x) - 0.5

    @staticmethod
    def round_to_only_half(x):
        # rounds to the nearest number which is divisible by 0.5 but not 1
        nearest_half = round(x * 2) / 2.0
        # Ensure it is not a whole number
        if nearest_half % 1 == 0:
            if x >= nearest_half:
                nearest_half += 0.5
            else:
                nearest_half -= 0.5
        return nearest_half

    @staticmethod
    def round_to_nearest_int_or_half(x):
        if abs(x - round(x)) == 0.5:
            return x
        return round(x)

    @staticmethod
    def general_quaternion_multiplication(a: tuple, b: tuple):
        return (
            a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
            a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
            a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],
            a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0]
        )

    @staticmethod
    def general_quaternion_division(a: tuple, b: tuple):
        # Calculate the product of the dividend 'a' and the multiplicative inverse of the divisor 'b'
        abinv = HurwitzQuaternion.general_quaternion_multiplication(a, HurwitzQuaternion.general_inverse(b))
        return abinv
