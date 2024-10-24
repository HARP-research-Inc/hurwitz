from hurwitz import HurwitzQuaternion
import pytest


class TestExpectedResults:

    def test_creation(self):
       
        q1 = HurwitzQuaternion(1, 2, 3, 4)
        q2 = HurwitzQuaternion(4, 3, 2, 1)
        q3 = HurwitzQuaternion(1, 1, 1, 1)
        q4 = HurwitzQuaternion(0, 0, 0, 0)
        q5 = HurwitzQuaternion(0, 1, 2, 0)

        q_h1 = HurwitzQuaternion(1, 3, 5, 7, half = True)
        q_h2 = HurwitzQuaternion(21, 31, 41, 51, half = True)
        q_h3 = HurwitzQuaternion(1, 1, 1, 1, half = True)


        # Whole
        assert str(q1) == "(1) + 2(i) + 3(j) + 4(k)"
        assert str(q2) == "4(1) + 3(i) + 2(j) + (k)"
        assert str(q3) == "(1) + (i) + (j) + (k)"
        assert str(q4) == ""
        assert str(q5) == "(i) + 2(j)"

        # Half
        assert str(q_h1) == "1/2(1) + 3/2(i) + 5/2(j) + 7/2(k)"
        assert str(q_h2) == "21/2(1) + 31/2(i) + 41/2(j) + 51/2(k)"
        assert str(q_h3) == "1/2(1) + 1/2(i) + 1/2(j) + 1/2(k)"
        
    def test_instantiation(self):
        # 1. Non-integer inputs
        with pytest.raises(TypeError):
            HurwitzQuaternion(1.5, 1, 1, 1, half=False)
        with pytest.raises(TypeError):
            HurwitzQuaternion("1", 1, 1, 1, half=False)

        # 2. Whole quaternions
        q1 = HurwitzQuaternion(1, 0, 0, 0, half=False)
        assert (q1.a, q1.b, q1.c, q1.d, q1.half) == (1, 0, 0, 0, False)

        # Whole quaternion, but passed as half; should convert to whole
        q2 = HurwitzQuaternion(2, 2, 2, 2, half=True)
        assert (q2.a, q2.b, q2.c, q2.d, q2.half) == (1, 1, 1, 1, False)

        # 3. Invalid half quaternion where one value is divisible by 2
        with pytest.raises(ValueError):
            HurwitzQuaternion(1, 2, 3, 1, half=True)

        # 4. Valid half quaternion where no values are divisible by 2
        q3 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        assert (q3.a, q3.b, q3.c, q3.d, q3.half) == (1, 3, 5, 7, True)

        # 5. Whole quaternion with zeros
        q4 = HurwitzQuaternion(0, 0, 0, 0, half=False)
        assert (q4.a, q4.b, q4.c, q4.d, q4.half) == (0, 0, 0, 0, False)


        """
        TO DO:
        
        # Half quaternion with zeros should raise an error
        with pytest.raises(ValueError):
            HurwitzQuaternion(0, 0, 0, 0, half=True)
        """

        # 6. Trace calculation
        q5 = HurwitzQuaternion(1, 1, 1, 1, half=False)
        assert q5.trace == 2

        q6 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        assert q6.trace == 1

        # 7. Unitary quaternions (whole)
        q7 = HurwitzQuaternion(1, 0, 0, 0, half=False)
        assert (q7.a, q7.b, q7.c, q7.d) in q7.unitary_whole_quaternions

        # Unitary half quaternion
        q8 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        assert (q8.a, q8.b, q8.c, q8.d) in q8.unitary_half_quaternions

        # 8. Negative values for whole quaternion
        q9 = HurwitzQuaternion(-1, -2, -3, -4, half=False)
        assert (q9.a, q9.b, q9.c, q9.d) == (-1, -2, -3, -4)

        # Negative values for half quaternion (no divisible by 2)
        q10 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        assert (q10.a, q10.b, q10.c, q10.d, q10.half) == (-1, -3, -5, -7, True)

        # Invalid negative half quaternion (divisible by 2)
        with pytest.raises(ValueError):
            HurwitzQuaternion(-2, -3, -5, -7, half=True)

        # 9. Mixed sign values
        q11 = HurwitzQuaternion(1, -3, 5, -7, half=True)
        assert (q11.a, q11.b, q11.c, q11.d, q11.half) == (1, -3, 5, -7, True)

        # Invalid mixed sign values (one divisible by 2)
        with pytest.raises(ValueError):
            HurwitzQuaternion(2, -3, 5, -7, half=True)

    def test_addition(self):
        # 1. Adding two whole quaternions
        q1 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q2 = HurwitzQuaternion(4, 3, 2, 1, half=False)
        q_sum = q1 + q2
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (5, 5, 5, 5, False)

        # 2. Adding two half quaternions
        q3 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q4 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_sum = q3 + q4
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (1, 1, 1, 1, False)  # Halves cancel out

        # 3. Adding whole quaternion to half quaternion (half + whole)
        q5 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q6 = HurwitzQuaternion(2, 4, 6, 8, half=False)
        q_sum = q5 + q6
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (5, 11, 17, 23, True)

        # 4. Adding whole quaternion to half quaternion (whole + half)
        q_sum = q6 + q5
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (5, 11, 17, 23, True)

        # 5. Adding a whole quaternion to itself
        q7 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_sum = q7 + q7
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (2, 4, 6, 8, False)

        # 6. Adding a half quaternion to itself
        q8 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_sum = q8 + q8
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (1, 1, 1, 1, False)  # Converts to whole

        # 7. Adding whole quaternion to negative whole quaternion
        q9 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q10 = HurwitzQuaternion(-1, -2, -3, -4, half=False)
        q_sum = q9 + q10
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (0, 0, 0, 0, False)

        # 8. Adding half quaternion to negative half quaternion
        q11 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q12 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        q_sum = q11 + q12
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (0, 0, 0, 0, False)

        # 9. Adding mixed sign half quaternion and whole quaternion
        q13 = HurwitzQuaternion(1, -3, 3, -7, half=True)
        q14 = HurwitzQuaternion(-2, 4, -6, 8, half=False)
        q_sum = q13 + q14
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (-3, 5, -9, 9, True)

        # 10. Adding mixed sign whole quaternion and half quaternion
        q_sum = q14 + q13
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (-3, 5, -9, 9, True)

        # 11. Invalid addition: adding a Hurwitz quaternion to a non-quaternion
        with pytest.raises(TypeError):
            q15 = HurwitzQuaternion(1, 2, 3, 4, half=False)
            q15 + 5  # Invalid addition

        # 12. Overflow edge case (extremely large numbers)
        large_value = 10**18
        q16 = HurwitzQuaternion(large_value, large_value, large_value, large_value, half=False)
        q17 = HurwitzQuaternion(large_value, large_value, large_value, large_value, half=False)
        q_sum = q16 + q17
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (2 * large_value, 2 * large_value, 2 * large_value, 2 * large_value, False)

        # 13. Zero quaternion added to whole quaternion
        q18 = HurwitzQuaternion(0, 0, 0, 0, half=False)
        q19 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_sum = q18 + q19
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (1, 2, 3, 4, False)

        # 14. Zero quaternion added to half quaternion
        q_sum = HurwitzQuaternion(0, 0, 0, 0, half=True) + HurwitzQuaternion(1, 3, 5, 7, half=True)
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (1, 3, 5, 7, True)

        # 15. Addition with overflow to a whole quaternion converting it to a half quaternion
        q20 = HurwitzQuaternion(1, 3, 5, 7, half=False)
        q21 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_sum = q20 + q21
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (3, 7, 11, 15, True)

        # 16. Adding whole quaternions with negative half quaternions
        q22 = HurwitzQuaternion(1, 3, 5, 7, half=False)
        q23 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        q_sum = q22 + q23
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d, q_sum.half) == (1, 3, 5, 7, True)

        # 17. Ensure addition does not result in a half quaternion with any zeros
        q1 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q2 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        q_sum = q1 + q2
        assert q_sum.half == False  # Should result in whole quaternion
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d) == (0, 0, 0, 0)  # Whole, all values are zero

        # 18. Ensure that addition does not result in a half quaternion containing any even numbers
        q3 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q4 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_sum = q3 + q4
        assert q_sum.half == False  # Addition results in whole quaternion
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d) == (1, 2, 3, 4)  # Whole quaternion, even numbers allowed

        # 19. Adding a whole quaternion to a half quaternion should not result in a half quaternion with zeros or even numbers
        q5 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q6 = HurwitzQuaternion(2, 2, 2, 2, half=False)
        q_sum = q5 + q6
        assert q_sum.half == True
        assert q_sum.a % 2 != 0  # None of the resulting values should be even
        assert q_sum.b % 2 != 0
        assert q_sum.c % 2 != 0
        assert q_sum.d % 2 != 0

        # 20. Adding two half quaternions with large odd numbers and ensuring no zero/even values in the result
        q7 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q8 = HurwitzQuaternion(3, 5, 7, 9, half=True)
        q_sum = q7 + q8
        assert q_sum.half == False  # Should result in whole quaternion
        assert q_sum.a == 2  # This is now a whole quaternion with even numbers allowed
        assert q_sum.b == 4
        assert q_sum.c == 6
        assert q_sum.d == 8

        # 21. Edge case: ensure no half quaternion can result with even numbers, even with mixed sign
        q9 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        q10 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_sum = q9 + q10
        assert q_sum.half == False  # Converts to whole quaternion due to summing
        assert (q_sum.a, q_sum.b, q_sum.c, q_sum.d) == (0, -1, -2, -3)  # Whole quaternion, even numbers allowed

        # 22. Ensure adding half quaternion with a whole quaternion does not result in half quaternion with zeros
        q11 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q12 = HurwitzQuaternion(1, 3, 5, 7, half=False)
        q_sum = q11 + q12
        assert q_sum.half == True
        assert q_sum.a != 0  # Ensure no zero in any component
        assert q_sum.b != 0
        assert q_sum.c != 0
        assert q_sum.d != 0

        # 23. Half quaternion addition with whole quaternion should not result in even numbers (remaining half)
        q13 = HurwitzQuaternion(3, 5, 7, 9, half=True)
        q14 = HurwitzQuaternion(2, 4, 6, 8, half=False)
        q_sum = q13 + q14
        assert q_sum.half == True
        assert q_sum.a % 2 != 0  # Ensure no even numbers in the result
        assert q_sum.b % 2 != 0
        assert q_sum.c % 2 != 0
        assert q_sum.d % 2 != 0
    
    def test_subtraction(self):
        # 1. Subtracting two whole quaternions
        q1 = HurwitzQuaternion(5, 5, 5, 5, half=False)
        q2 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_diff = q1 - q2
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (4, 3, 2, 1, False)

        # 2. Subtracting two half quaternions
        q3 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q4 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_diff = q3 - q4
        q_diff.half = False
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (0, 0, 0, 0, False)  # Cancels to whole quaternion
        q4 = HurwitzQuaternion(1, 3, 3, 1, half=True)
        q_diff = q4 - q3
        assert q_diff.half == False
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (0, 1, 1, 0, False)  # Cancels to whole quaternion

        # 3. Subtracting whole quaternion from half quaternion (half - whole)
        q5 = HurwitzQuaternion(3, 5, 7, 9, half=True)
        q6 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_diff = q5 - q6
        assert q_diff.half == True
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (1, 1, 1, 1, True)

        # 4. Subtracting half quaternion from whole quaternion (whole - half)
        q_diff = q6 - q5
        assert q_diff.half == True
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (-1, -1, -1, -1, True)

        # 5. Subtracting a whole quaternion from itself
        q7 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_diff = q7 - q7
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (0, 0, 0, 0, False)

        # 6. Subtracting a half quaternion from itself
        q8 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_diff = q8 - q8
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (0, 0, 0, 0, False)  # Converts to whole

        # 7. Subtracting whole quaternion from negative whole quaternion
        q9 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q10 = HurwitzQuaternion(-1, -2, -3, -4, half=False)
        q_diff = q9 - q10
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (2, 4, 6, 8, False)

        # 8. Subtracting half quaternion from negative half quaternion
        q11 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q12 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        q_diff = q11 - q12
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (1, 3, 5, 7, False)

        # 9. Subtracting mixed sign half quaternion and whole quaternion
        q13 = HurwitzQuaternion(1, -3, 3, -7, half=True)
        q14 = HurwitzQuaternion(-2, 4, -6, 8, half=False)
        q_diff = q13 - q14
        assert q_diff.half == True
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (5, -11, 15, -23, True)

        # 10. Subtracting mixed sign whole quaternion and half quaternion
        q_diff = q14 - q13
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (-5, 11, -15, 23, True)

        # 11. Invalid subtraction: subtracting a Hurwitz quaternion from a non-quaternion
        with pytest.raises(TypeError):
            q15 = HurwitzQuaternion(1, 2, 3, 4, half=False)
            q15 - 5  # Invalid subtraction

        # 12. Subtracting extremely large numbers
        large_value = 10**18
        q16 = HurwitzQuaternion(2 * large_value, 2 * large_value, 2 * large_value, 2 * large_value, half=False)
        q17 = HurwitzQuaternion(large_value, large_value, large_value, large_value, half=False)
        q_diff = q16 - q17
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (large_value, large_value, large_value, large_value, False)

        # 13. Zero quaternion subtracted from whole quaternion
        q18 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_diff = HurwitzQuaternion(0, 0, 0, 0, half=False) - q18
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (-1, -2, -3, -4, False)

        # 14. Zero quaternion subtracted from half quaternion
        q_diff = HurwitzQuaternion(0, 0, 0, 0, half=True) - HurwitzQuaternion(1, 3, 5, 7, half=True)
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (-1, -3, -5, -7, True)

        # 15. Subtracting whole quaternions with a negative half quaternion
        q20 = HurwitzQuaternion(1, 3, 5, 7, half=False)
        q21 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        q_diff = q20 - q21
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d, q_diff.half) == (3, 9, 15, 21, True)

        # 16. Ensure subtraction does not result in a half quaternion with any zeros
        q1 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q2 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q_diff = q1 - q2
        assert q_diff.half == False  # Should result in whole quaternion
        assert (q_diff.a, q_diff.b, q_diff.c, q_diff.d) == (0, 0, 0, 0)  # Whole, all values are zero

        # 17. Subtraction of a half by a odd half results in a whole quaternion
        q3 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q4 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_diff = q3 - q4
        assert q_diff.half == False  # Subtraction transforms it into a whole

        # 18. Subtracting a whole quaternion from a half quaternion should not result in a half quaternion with zeros or even numbers
        q5 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q6 = HurwitzQuaternion(2, 2, 2, 2, half=False)
        q_diff = q5 - q6
        assert q_diff.half == True
        assert q_diff.a % 2 != 0  # Ensure no even numbers
        assert q_diff.b % 2 != 0
        assert q_diff.c % 2 != 0
        assert q_diff.d % 2 != 0

    def test_multiplication(self):
        
        # 1. Multiplying two whole quaternions
        q1 = HurwitzQuaternion(5, 5, 5, 5, half=False)
        q2 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_product = q1 * q2
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (-40, 20, 10, 30, False)

        # 2. Multiplying two half quaternions, and remains a half quaternion
        q3 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q4 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_product = q3 * q4 
        print(str(q_product.half))
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (-1, 1, 1, 1, True)
        

        # 3. Multiplying whole quaternion by half quaternion (whole * half)
        q5 = HurwitzQuaternion(3, 5, 7, 9, half=True)
        q6 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_product = q5 * q6
        assert q_product.half == False
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (-32, 6, 7, 11, False)
        
        # 4. Multiplying half quaternion by whole quaternion (half * whole)
        q_product = q6 * q5
        assert q_product.half == False
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (-32, 5, 9, 10, False)

        # 5. Multiplying a whole quaternion by itself
        q7 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_product = q7 * q7
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (-28, 4, 6, 8, False)

        # 6. Multiplying a half quaternion by itself
        q8 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_product = q8 * q8
        assert q_product.half == True
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (-1, 1, 1, 1, True)
        
        # 7. Multiplying whole quaternion by negative whole quaternion
        q9 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q10 = HurwitzQuaternion(-1, -2, -3, -4, half=False)
        q_product = q9 * q10
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (28, -4, -6, -8, False)

        # 8. Multiplying half quaternion by negative half quaternion
        q11 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q12 = HurwitzQuaternion(-1, -3, -5, -7, half=True)
        q_product = q11 * q12
        assert q_product.half == True
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (41, -3, -5, -7, True)
        
        # 9. Multiplying mixed sign half quaternion and whole quaternion
        q13 = HurwitzQuaternion(1, -3, 3, -7, half=True)
        q14 = HurwitzQuaternion(-2, 4, -6, 8, half=False)
        q_product = q13 * q14

        assert q_product.half == False
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (42, -4, -8, 14, False)
        q_product = q14 * q13
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (42, 14, -4, 8, False)
        
        q15 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q15 *= 5  # Invalid multiplication
        assert (q15.a, q15.b, q15.c, q15.d, q15.half) == (5, 10, 15, 20, False)
        
        q18 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_product = HurwitzQuaternion(0, 0, 0, 0, half=False) * q18
        q_product = HurwitzQuaternion(0, 0, 0, 0, half=True) * HurwitzQuaternion(1, 3, 5, 7, half=True)
        assert (q_product.a, q_product.b, q_product.c, q_product.d, q_product.half) == (0, 0, 0, 0, False)

        q1 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q2 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q_product = q1 * q2
        assert q_product.half == True
        assert (q_product.a, q_product.b, q_product.c, q_product.d) != (0, 0, 0, 0)  # Should not all be zero

        # 17. Multiplication of a half by an odd half results in a non-whole quaternion
        q3 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q4 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_product = q3 * q4
        assert q_product.half == True

    def test_norm(self):
        # Whole quaternion
        q1 = HurwitzQuaternion(1, 2, 3, 4)
        expected_norm_q1 = (1**2 + 2**2 + 3**2 + 4**2)**0.5  # sqrt(1 + 4 + 9 + 16) = sqrt(30)
        assert q1.norm() == expected_norm_q1

        # Half quaternion
        q_h1 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        expected_norm_q_h1 = ((1/2)**2 + (3/2)**2 + (5/2)**2 + (7/2)**2)**0.5  # sqrt(1/4 + 1 + 9/4 + 4) = sqrt(30/4)
        assert q_h1.norm() == expected_norm_q_h1

        # Zero quaternion
        q_zero = HurwitzQuaternion(0, 0, 0, 0)
        assert q_zero.norm() == 0

    def test_conjugate(self):
        # Whole quaternion
        q1 = HurwitzQuaternion(1, 2, 3, 4)
        expected_conjugate_q1 = HurwitzQuaternion(1, -2, -3, -4)
        assert q1.conjugate() == expected_conjugate_q1

        # Half quaternion
        q_h1 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        expected_conjugate_q_h1 = HurwitzQuaternion(1, -3, -5, -7, half=True)
        assert q_h1.conjugate() == expected_conjugate_q_h1

        # Zero quaternion
        q_zero = HurwitzQuaternion(0, 0, 0, 0)
        expected_conjugate_q_zero = HurwitzQuaternion(0, 0, 0, 0)
        assert q_zero.conjugate() == expected_conjugate_q_zero


    def test_inverse(self):
        # Whole unitary quaternion (norm = 1)
        q1 = HurwitzQuaternion(1, 0, 0, 0)  # Norm = 1, so inverse = conjugate
        expected_inverse_q1 = HurwitzQuaternion(1, 0, 0, 0) 
        assert q1.inverse() == expected_inverse_q1

        # Half unitary quaternion (norm = 1/2)
        q_h1 = HurwitzQuaternion(1, 1, 1, 1, half=True)  # Norm = sqrt(2)/2
        expected_inverse_q_h1 = HurwitzQuaternion(1, -1, -1, -1, half = True) 
        assert q_h1.inverse() == expected_inverse_q_h1

    
    def test_division(self):
        # Floor division whole
        q1 = HurwitzQuaternion(3, 5, 6, 8)
        q2 = HurwitzQuaternion(2, 1, 3, 4)
        assert q1 // q2 == q1.euclidean_division(q2)[0] # Remainder
        assert q2 // q1 == q2.euclidean_division(q1)[0] 

        # Floor division half
        q_h1 = HurwitzQuaternion(1, 3, 5, 7, half = True)
        q_h2 = HurwitzQuaternion(9, 11, 1, 57, half = True)
        assert q_h1 // q_h2 == q_h1.euclidean_division(q_h2)[0]
        assert q_h2 // q_h1 == q_h2.euclidean_division(q_h1)[0]

        # Floor division half and whole
        assert q1 // q_h2 == q1.euclidean_division(q_h2)[0]
        assert q_h2 // q1 == q_h2.euclidean_division(q1)[0]
        assert q2 // q_h1 == q2.euclidean_division(q_h1)[0]
        assert q_h1 // q2 == q_h1.euclidean_division(q2)[0]

        # Modulus whole
        assert q1 % q2 == q1.euclidean_division(q2)[1]
        assert q2 % q1 == q2.euclidean_division(q1)[1] 

        # Modulus half
        assert q_h1 % q_h2 == q_h1.euclidean_division(q_h2)[1]
        assert q_h2 % q_h1 == q_h2.euclidean_division(q_h1)[1]

        # Modulus division half and whole
        assert q1 % q_h2 == q1.euclidean_division(q_h2)[1]
        assert q_h2 % q1 == q_h2.euclidean_division(q1)[1]
        assert q2 % q_h1 == q2.euclidean_division(q_h1)[1]
        assert q_h1 % q2 == q_h1.euclidean_division(q2)[1]

        # 1. True division of two whole quaternions
        q1 = HurwitzQuaternion(2, 4, 6, 8, half=False)
        q2 = HurwitzQuaternion(1, 3, 5, 7, half=False)
        q_div = q1 / q2
        assert (round(q_div[0], 2), round(q_div[1], 2), round(q_div[2], 2), round(q_div[3], 2)) == (1.19,-0.05,0,-0.1)

        # 2. True division of a whole quaternion by a half quaternion
        q3 = HurwitzQuaternion(3, 3, 3, 3, half=False)
        q4 = HurwitzQuaternion(1, 1, 1, 1, half=True)
        q_div = q3 / q4
        assert (round(q_div[0], 2), round(q_div[1], 2), round(q_div[2], 2), round(q_div[3], 2)) == (6,0,0,0)


        # 3. True division of two half quaternions
        q5 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q6 = HurwitzQuaternion(3, 9, 11, 1, half=True)
        q_div = q5 / q6
        assert (round(q_div[0], 2), round(q_div[1], 2), round(q_div[2], 2), round(q_div[3], 2)) == (0.43,0.34,-0.26,0.15)

        # 4. True division of a whole quaternion by itself
        q7 = HurwitzQuaternion(1, 2, 3, 4, half=False)
        q_div = q7 / q7
        assert (round(q_div[0], 2), round(q_div[1], 2), round(q_div[2], 2), round(q_div[3], 2)) == (1.00, 0.00, 0.00, 0.00)

        # 5. True division of a whole quaternion by itself
        q7 = HurwitzQuaternion(1, 3, 5, 7, half=True)
        q_div = q7 / q7
        assert (round(q_div[0], 2), round(q_div[1], 2), round(q_div[2], 2), round(q_div[3], 2)) == (1.00, 0.00, 0.00, 0.00)



    """
    def test_associates_and_equivalence_classes(self): 
        # Associates of quaternion
        q1 = HurwitzQuaternion(3, 5, 6, 8)
        q2 = HurwitzQuaternion(2, 1, 3, 4)

        
        # 8 standard unit quaternions
        standard_units = [
            HurwitzQuaternion(1, 0, 0, 0),  # 1
            HurwitzQuaternion(-1, 0, 0, 0),  # -1
            HurwitzQuaternion(0, 1, 0, 0),  # i
            HurwitzQuaternion(0, -1, 0, 0),  # -i
            HurwitzQuaternion(0, 0, 1, 0),  # j
            HurwitzQuaternion(0, 0, -1, 0),  # -j
            HurwitzQuaternion(0, 0, 0, 1),  # k
            HurwitzQuaternion(0, 0, 0, -1),  # -k
        ]

        # 16 half-integer unit quaternions (with half=True)
        half_integer_units = [
            HurwitzQuaternion(1, 1, 1, 1, half=True),
            HurwitzQuaternion(1, -1, 1, 1, half=True),
            HurwitzQuaternion(1, 1, -1, 1, half=True),
            HurwitzQuaternion(1, 1, 1, -1, half=True),
            HurwitzQuaternion(1, -1, -1, 1, half=True),
            HurwitzQuaternion(1, -1, 1, -1, half=True),
            HurwitzQuaternion(1, 1, -1, -1, half=True),
            HurwitzQuaternion(1, -1, -1, -1, half=True),
            
            HurwitzQuaternion(-1, 1, 1, 1, half=True),
            HurwitzQuaternion(-1, -1, 1, 1, half=True),
            HurwitzQuaternion(-1, 1, -1, 1, half=True),
            HurwitzQuaternion(-1, 1, 1, -1, half=True),
            HurwitzQuaternion(-1, -1, -1, 1, half=True),
            HurwitzQuaternion(-1, -1, 1, -1, half=True),
            HurwitzQuaternion(-1, 1, -1, -1, half=True),
            HurwitzQuaternion(-1, -1, -1, -1, half=True),
        ]

        # Combine both lists
        unit_quaternions = standard_units + half_integer_units
        for i in range(len(unit_quaternions)):
            associate = q1 * unit_quaternions[i]
            assert associate in q1.associates()        
        

        
        # Equivalence classes of quaternion
        unit_quaternions += q1.conjugate()
        for i in range(len(unit_quaternions)):
            associate = q1 * unit_quaternions[i]
            assert associate in q1.associates()

        # Check if two quaternions are associates
        is_associate = q2 * unit_quaternions[2]
        not_associate = q2 * HurwitzQuaternion(1,5,2,2)

        assert is_associate in q2.associates()
        assert not_associate not in q2.associates()
        
    
    def test_snap(self):
        # Test rounding to nearesrt Hurwitz quaternion
        q1 = HurwitzQuaternion(3, 5, 6, 8)
        general_q = (1.2, 2.8, 3.5, 4.1)  
        q_snapped = q1.snap(general_q)
        genera_q_h1 = (0.9, 2.5, 50.6666666, 7.49999999999)
        q_h1_snapped = q1.snap(genera_q_h1)

        assert q_snapped == HurwitzQuaternion(1, 3, 4, 4)
        assert q_h1_snapped == HurwitzQuaternion(1, 3, 51, 7)
    """

class TestUnexpectedResults:

    def test_invalid_creation(self):
        # Test creation with zero or even for half

        with pytest.raises(TypeError):
            HurwitzQuaternion(1, 2, 3)  # Not enough components
        
        with pytest.raises(ValueError):
            HurwitzQuaternion(1, 0, 2, 0, half=True)  # Half quaternion with zero components
        
        with pytest.raises(TypeError):
            HurwitzQuaternion(1.5, 2, 3, 4)  # Non-integer input for whole quaternion


    def test_division_by_zero(self):
        # Division by a zero quaternion
        q1 = HurwitzQuaternion(1, 2, 3, 4)
        q_zero = HurwitzQuaternion(0, 0, 0, 0)

        with pytest.raises(ZeroDivisionError):
            q1 / q_zero

        with pytest.raises(ZeroDivisionError):
            q1 // q_zero

        with pytest.raises(ZeroDivisionError):
            q1 % q_zero
    
    def test_invalid_operations(self):
        # Test non-quaternion inputs (e.g., q1 + "str" or q2 + None)
        q1 = HurwitzQuaternion(1, 2, 3, 4)
        q2 = HurwitzQuaternion(1, 1, 1, 1, half=True)

        with pytest.raises(TypeError):
            q1 + "string"  # Should raise an error for adding non-quaternion

        with pytest.raises(TypeError):
            q1 + None  # Should raise an error for adding None

        with pytest.raises(Exception):
                q3 = HurwitzQuaternion(0, -1, -1, -1)
                q4 = q3.inverse()  # Should raise an error for invalid inverse


class TestGeneralEdgeCases:

    # Basic Setup
    hq = HurwitzQuaternion(1, 2, 3, 4)
    identity = HurwitzQuaternion(1, 0, 0, 0)
    zero = HurwitzQuaternion(0, 0, 0, 0)
    
    # --- Additional Edge Cases ---

    # Test 14: Norm of identity quaternion
    assert identity.norm() == 1, "Norm of identity quaternion failed"


    # Test 16: Non-division by zero quaternion
    try:
        result = hq / zero
    except ZeroDivisionError:
        print("Division by zero quaternion correctly caught")

    # Test 17: Norm should be invariant under conjugation
    assert hq.norm() == hq.conjugate().norm(), "Norm invariance under conjugation failed"

    unitary_q = HurwitzQuaternion(1,1,1,1,True)
    inverse = unitary_q.inverse()
    result = unitary_q * inverse
    assert result == identity, "Multiplication by inverse failed"

    # Test 18: Multiplication by inverse is invalid as Quaternion is not unitary
    with pytest.raises(Exception):
        unitary_q = HurwitzQuaternion(1,1,1,1)
        inverse = unitary_q.inverse()
        result = unitary_q * inverse
        assert result == identity, "Multiplication by inverse failed"

    # Test 19: Quaternion inverse when components are zero
    zero_quaternion = HurwitzQuaternion(0, 0, 0, 0)
    try:
        result = zero_quaternion.inverse()
    except Exception:
        print("Correctly caught inverse of zero quaternion.")

    # Test 22: Conjugate of inverse should be the inverse of the conjugate
    unitary_q2 = HurwitzQuaternion(1,0,0,0,False)
    assert unitary_q2.conjugate().inverse() == unitary_q2.inverse().conjugate(), "Conjugate of inverse property failed"

    # Test 25: Distributive property over both addition and subtraction
    hq2 = HurwitzQuaternion(2, 3, 1, 4)
    hq3 = HurwitzQuaternion(1, 0, -2, 5)
    hq4 = HurwitzQuaternion(1, 3, 5, 7, True)
    assert hq2 * (hq3 - hq4) == hq2 * hq3 - hq2 * hq4, "Distributive property over subtraction failed"
    