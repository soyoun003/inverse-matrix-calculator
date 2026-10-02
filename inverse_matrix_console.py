# Inverse Matrix Calculator


# Matrix Input

n = int(input("Enter n: "))

A = []

print("Enter the matrix row by row:")

for i in range(n):
    row = list(map(int, input(f"Row {i + 1}: ").split()))
    A.append(row)

print("\nInput Matrix:")

for row in A:
    print(row)


# Explanation:
# The program asks the user to enter the size n.
# Then, the user enters the n × n matrix row by row.
# The matrix is stored as a two-dimensional list.


# Calculate Determinant Using Gaussian Elimination

def det(A):

    M = [row[:] for row in A]
    n = len(M)

    determinant = 1
    swaps = 0

    for i in range(n):

        pivot = max(
            range(i, n),
            key=lambda r: abs(M[r][i])
        )

        if abs(M[pivot][i]) < 1e-10:
            return 0

        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
            swaps += 1

        for r in range(i + 1, n):

            factor = M[r][i] / M[i][i]

            for c in range(i, n):
                M[r][c] -= factor * M[i][c]

    for i in range(n):
        determinant *= M[i][i]

    if swaps % 2 == 1:
        determinant = -determinant

    return determinant


# Explanation:
# This function calculates the determinant using
# Gaussian Elimination.
#
# The matrix is transformed into an upper triangular
# matrix by eliminating the values below each pivot.
#
# The determinant is the product of the diagonal elements.
#
# If rows are swapped, the sign of the determinant changes.
#
# The value 1e-10 is used as a small tolerance for
# floating-point calculations.


# Inverse Using Determinant

def inverse_det(A):

    n = len(A)
    d = det(A)

    if abs(d) < 1e-10:
        return None

    if n == 1:
        return [[1 / d]]

    if n == 2:
        return [
            [A[1][1] / d, -A[0][1] / d],
            [-A[1][0] / d, A[0][0] / d]
        ]

    cof = []

    for i in range(n):

        row = []

        for j in range(n):

            minor = [
                r[:j] + r[j + 1:]
                for k, r in enumerate(A)
                if k != i
            ]

            row.append(
                (-1) ** (i + j) * det(minor)
            )

        cof.append(row)

    return [
        [cof[j][i] / d for j in range(n)]
        for i in range(n)
    ]


# Explanation:
# This function calculates the inverse using
# the determinant and adjugate matrix.
#
# The formula is:
#
# A^-1 = adj(A) / det(A)
#
# If the determinant is zero, the inverse does not exist.
#
# For a 2 × 2 matrix, the standard inverse formula is used.
#
# For larger matrices, the cofactor matrix is calculated.
# Then, the cofactor matrix is transposed to obtain
# the adjugate matrix.


# Inverse Using Gauss-Jordan Elimination

def inverse_gj(A):

    n = len(A)

    M = [
        [float(x) for x in A[i]] +
        [1.0 if i == j else 0.0 for j in range(n)]
        for i in range(n)
    ]

    for i in range(n):

        pivot = max(
            range(i, n),
            key=lambda r: abs(M[r][i])
        )

        if abs(M[pivot][i]) < 1e-10:
            return None

        M[i], M[pivot] = M[pivot], M[i]

        p = M[i][i]

        M[i] = [x / p for x in M[i]]

        for r in range(n):

            if r != i:

                factor = M[r][i]

                M[r] = [
                    M[r][c] - factor * M[i][c]
                    for c in range(2 * n)
                ]

    return [row[n:] for row in M]


# Explanation:
# This function calculates the inverse using
# Gauss-Jordan Elimination.
#
# The augmented matrix [A | I] is created.
#
# The row operations transform:
#
# [A | I] → [I | A^-1]
#
# When the left side becomes the identity matrix,
# the right side contains the inverse matrix.


# Display Matrix

def show(M):

    for row in M:

        print(" ".join(
            str(int(round(x)))
            if abs(x - round(x)) < 1e-10
            else str(round(x, 3))
            for x in row
        ))


# Explanation:
# This function displays the matrix clearly.
#
# Integer values are displayed without decimal places.
# Decimal values are displayed with up to three decimal places.
#
# For example:
# 1.0 is displayed as 1
# 0.333333 is displayed as 0.333


# Verify A × A^-1 = I

def verify_inverse(A, inverse):

    n = len(A)

    for i in range(n):

        for j in range(n):

            value = 0

            for k in range(n):
                value += A[i][k] * inverse[k][j]

            expected = 1 if i == j else 0

            if abs(value - expected) > 1e-8:
                return False

    return True


# Explanation:
# This function checks the inverse mathematically.
#
# It calculates A × A^-1.
#
# If the result is the identity matrix I,
# the inverse is successfully verified.


# Main Program

d = det(A)

print("\nDeterminant =", round(d, 10))


# Determinant Method

print("\n[Determinant Method]")

inv1 = inverse_det(A)

if inv1 is None:
    print("Inverse does not exist.")
else:
    show(inv1)


# Explanation:
# The inverse is calculated using the determinant method.
# If the determinant is zero, an error message is displayed.
# Otherwise, the inverse matrix is displayed.


# Gauss-Jordan Method

print("\n[Gauss-Jordan Method]")

inv2 = inverse_gj(A)

if inv2 is None:
    print("Inverse does not exist.")
else:
    show(inv2)


# Explanation:
# The inverse is calculated again using
# Gauss-Jordan Elimination.
# The result is displayed separately.


# Compare the Two Results

if inv1 is not None and inv2 is not None:

    same = all(
        abs(inv1[i][j] - inv2[i][j]) < 1e-8
        for i in range(n)
        for j in range(n)
    )

    print("\n[Comparison]")

    if same:
        print("The two results are identical.")
    else:
        print("The two results are different.")


# Explanation:
# The two inverse matrices are compared element by element.
# A small tolerance is used because floating-point calculations
# may contain very small numerical errors.
#
# If all corresponding elements are sufficiently close,
# the program reports that the two results are identical.


# Verification

if inv2 is not None:

    print("\n[Verification]")

    if verify_inverse(A, inv2):
        print("A × A^-1 = I")
        print("Inverse matrix verified successfully.")
    else:
        print("Verification failed.")


# Explanation:
# The program multiplies the original matrix by its inverse.
#
# If the result is the identity matrix,
# the program confirms that the inverse is correct.