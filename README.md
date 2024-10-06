## `<img src="https://static.wixstatic.com/media/355b75_1c4e29d87f1e449cbdfdb2b623ac66ce~mv2.png/v1/fill/w_292,h_72,fp_0.50_0.50,q_85,usm_0.66_1.00_0.01,enc_auto/355b75_1c4e29d87f1e449cbdfdb2b623ac66ce~mv2.png" width="100">` research, Inc. - **Hurwitz**

## Hurwitz

A Hurwitz Quaternion Integer Library for Python - Made by Harper Chisari

## Installation

Currently, Hurwitz is easy to install, as it has no dependencies. This is likely to change soon with a significant extension on the way.

You can install the Hurwitz package from PyPI using pip:

```bash
pip install hurwitz
```

## Usage

First, import the `HurwitzQuaternion` class from the Hurwitz package:

```python
from hurwitz import HurwitzQuaternion
```

You can create a Hurwitz quaternion by instantiating the `HurwitzQuaternion` class with four integer values:

```python
q1 = HurwitzQuaternion(1, 2, 3, 4) # 1 + 2i + 3j + 4k
q2 = HurwitzQuaternion(2, 3, 4, 5) # 2 + 3i + 4j + 5k
```

If you want to create a half quaternion, set the half parameter to True:

```python
q_half = HurwitzQuaternion(1, 3, 5, 7, half=True)
```

> [!IMPORTANT]
> Half-Integer quaternions *cannot* accept zeroes nor even values as coefficients. Those would lead to a *non-Hurwitz quaternion*. If you want to get to the 'closest' quaternion, use the `snap` method below.

## Basic Operations

Simple operations on Hurwitz Integers are easy in Hurwitz!

### Addition, Subtraction, and Multiplication

```python
q3 = q1 + q2
print(q3)  # Output: 3 + 5i + 7j + 9ij

q4 = q1 - q2
print(q4)  # Output: -1 + -1i + -1j + -1ij

q5 = q1 * q2
print(q5)  # Output: -36 + 6i + 12j + 12ij

q6 = q1 * 2
print(q6)  # Output: 2 + 4i + 6j + 8ij
```

Hurwitz currently only supports integer multiplication, mostly because it made subtraction easier to implement.

### Norm, Conjugate, and Inverse

#### Norm

The norm in Hurwitz is defined as:

$$
\text{Nr}(q) = 
\begin{cases} 
\sqrt{a^2 + b^2 + c^2 + d^2} & \text{if } q \text{ is a whole quaternion} \\
\sqrt{\left(\frac{a}{2}\right)^2 + \left(\frac{b}{2}\right)^2 + \left(\frac{c}{2}\right)^2 + \left(\frac{d}{2}\right)^2} & \text{if } q \text{ is a half quaternion}
\end{cases}
$$

and can be simply calculated with

`q1.norm()`

#### Conjugate

The conjugate of a Hurwitz quaternion \( q = a + bi + cj + dk \) is defined as:

$$
\text{Conj}(q) = a - bi - cj - dk
$$

For half quaternions, the conjugate is:

$$
\text{Conj}(q) = \frac{a}{2} - \frac{b}{2}i - \frac{c}{2}j - \frac{d}{2}k
$$

You can calculate the conjugate using `q1.conjugate()`

#### Inverse

The inverse of a unitary Hurwitz quaternion \( q \) is defined as the conjugate of \( q \) divided by the norm of \( q \) squared.

For Hurwitz quaternions, this includes *only* the 24 units:

$$
\pm 1, \pm i, \pm j, \pm k, \frac{ \pm 1 \pm i \pm j \pm k}{2} .
$$

For a non-unitary quaternion, the general inverse is calculated as:

$$
\text{Inv}(q) = \frac{\text{Conj}(q)}{\text{Nr}(q)^2}
$$

For unitary quaternions, you can calculate the inverse using `q1.inverse()`

### Example Code

Here’s how you can demonstrate these calculations using the `hurwitz` package:

```python
from hurwitz import HurwitzQuaternion

# Create a Hurwitz quaternion
q1 = HurwitzQuaternion(1, 2, 3, 4)

# Calculate the norm
norm_q1 = q1.norm()
print("Norm of q1:", norm_q1)

# Calculate the conjugate
conj_q1 = q1.conjugate()
print("Conjugate of q1:", conj_q1)

# Calculate the inverse (only if q1 is unitary)
try:
    inv_q1 = q1.inverse()
    print("Inverse of q1:", inv_q1)
except ValueError as e:
    print(e)
```

### General Quaternion Operations

Hurwitz does support transformation to 'general' quaternions in the form of a 4-tuple.
In order to do so, simply invoke the `general` method:

```python
q1_general = q1.general
print(q1_general) # prints a tuple (1, 2, 3, 4)
```

This includes the `general_inverse`, `general_quaternion_multiplication`, and `general_quaternion_division` methods. These naturally also return 4-tuples.

## Advanced Operations

### Division

Yes! Division of Hurwitz integers! Admittedly, just as with regular integers, this is implemented as Euclidean division.

The Euclidean division can either be accessed directly as `euclidean_division` or in components using the `//` floordiv and `%` modulo operators.

```python
q7 = q1 // q2  # Floor division
print(q7)  # Output: 2

q8 = q1 % q2  # Modulus
print(q8) # Output: -2 - 2i - 2j - 2k

q9 = q1.euclidean_division(q2)  # Euclidean division
print(q9)  # Output: (2, -2 - 2i - 2j - 2k)

q8 = q1 / q2  # True division
print(q8)  # Output: (0.74, 0.037, 0.0, 0.074)
```

Citation: For more on Euclidean division in the context of Hurwitz quaternions and to see the source of the algorithm used, see: [Boyd Coan and Cherng-tiao Perng, &#34;Factorization of Hurwitz Quaternions,&#34; International Mathematical Forum, Vol. 7, 2012, no. 43, 2143 - 2156.](https://m-hikari.com/imf/imf-2012/41-44-2012/perngIMF41-44-2012.pdf)

### (Int) Powers

Currently, you can raise Hurwitz quaternions to integer powers. In the future we will add quaternion power support, and potentially fractional and logarithm support.

### Decomposition

Decomposition is simply a method for decomposing a Hurwitz quaternion into unitary ones. This generally consists of a few whole Hurwitz quaternions and a single half quaternion unit.

```python
print("Decomposition of q1:", q1.decompose()) # results in 1 + 2 + 3 + 4 = 10 whole unit Hurwitz quaternions

q_half_ex = HurwitzQuaternion(1,3,5,7, half=True) # 1/2 + 3/2 i + 5/2 j + 7/2 k

print("Half quaternion:", repr(q_half_ex))
print("Decomposition of q1:" )
for val in q_half_ex.decompose():
    print(repr(val)) 
# Output: 0 + 1i + 0j + 0ij, 0 + 0i + 1j + 0ij, 0 + 0i + 1j + 0ij0 + 0i + 0j + 1ij
# 0 + 0i + 0j + 1ij, 0 + 0i + 0j + 1ij, 1/2 + 1/2i + 1/2j + 1/2ij
```

### Associates and Equivalence Classes

Associates of a Hurwitz Quaternion are defined as the quaternion multiplied by any of teh unit quaternuions, meaning that the Norm stays the same.

You can find all associates of a quaternion:

```python
associates = q1.associates()
print("Associates of q1:", associates)
```

You can also find the equivalence class, the associates of a quaternion and it's conjugate:

```python
equivalence_class = q1.equivalence_class()
print("Equivalence Class of q1:", equivalence_class)
```

### Association Check

To check if two quaternions are associates:

```python
q3 = HurwitzQuaternion(2, 3, 4, 5)
is_associate = q1.association_check(q1, q3)
print("Are q1 and q3 associates?", is_associate)
```

## Bonus Features

### Binomial Decomposition

You can can the `binomial_composition()` method to retrieve a tuple of the largest whole hurwitz quaternion and smallest half integer quaternion which can be added to get the given quaternion.

### Euclidean Division Pro Max

This method attempts to divide the conjugate of the dividend by the divisor and returns the result with the smallest remainder:

```python
q7_pro, r_pro = q1.euclidean_division_pro_max(q2)
print("Quotient (Pro Max) (q7_pro):", q7_pro)
print("Remainder (Pro Max) (r_pro):", r_pro)
```

### Snap: Rounding to the Nearest Hurwitz Quaternion

The snap method rounds the values of a general quaternion to the nearest integer or half:

```python
general_q = (1.2, 2.8, 3.5, 4.1)
q_snapped = q1.snap(general_q)
print("Snapped Quaternion:", q_snapped)
```

### Symbolic String

The Hurwitz library also supports a new symbolic string representation via the `symbolic_rep` method.
This is for something down the road!

## Planned Features

In the near-future the library will support:

- H. Quaternion matrices and operations
- H. Quaternion factorization and Norm rings
- more primality-related features
- C-based, and CUDA performance improvements for parallel operations
- Qiskit integration for hypercomplex-quantum mechanics
- Generalized operations on Clifford Algebras

${\color{grey}\textsf{Copyright © 2024 HARP research, Inc. Visit us at }}$ [https://harpresearch.ai](https://harpresearch.ai)
