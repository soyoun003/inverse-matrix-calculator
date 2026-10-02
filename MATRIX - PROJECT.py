import tkinter as tk
from tkinter import messagebox


# Matrix Input

def create_matrix():
    try:
        n = int(size_entry.get())

        if n < 1:
            raise ValueError

        for widget in matrix_frame.winfo_children():
            widget.destroy()

        matrix_entries.clear()

        for i in range(n):
            row = []

            for j in range(n):
                entry = tk.Entry(
                    matrix_frame,
                    width=8,
                    justify="center"
                )
                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )
                row.append(entry)

            matrix_entries.append(row)

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter a positive integer for n."
        )


# Explanation:
# This function creates an n × n input table.
# The user first enters the size of the matrix.
# Then, the program creates an Entry widget
# for every element of the matrix.


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
# The determinant is the product of the diagonal
# elements of the triangular matrix.
#
# If rows are swapped, the sign of the determinant
# changes.
#
# A small tolerance of 1e-10 is used to handle
# floating-point calculation errors.


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
# If the determinant is zero, the inverse
# does not exist.
#
# For larger matrices, the program creates
# the cofactor matrix and transposes it
# to obtain the adjugate matrix.


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
# Through elementary row operations:
#
# [A | I] → [I | A^-1]
#
# The left side becomes the identity matrix,
# and the right side becomes the inverse matrix.


# Display Matrix

def format_matrix(M):

    result = ""

    for row in M:

        formatted_row = []

        for x in row:

            if abs(x - round(x)) < 1e-10:
                formatted_row.append(str(int(round(x))))
            else:
                formatted_row.append(str(round(x, 3)))

        result += "[ " + "   ".join(formatted_row) + " ]\n"

    return result


# Explanation:
# This function converts a matrix into a clean
# text format for displaying it in the GUI.
#
# Integer values are displayed without decimal places.
# Decimal values are displayed up to three places.


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
# This function verifies the inverse mathematically.
#
# It calculates:
#
# A × A^-1
#
# and checks whether the result is the identity matrix I.
#
# If every element matches the identity matrix,
# the function returns True.


# Calculate Everything

def calculate():

    try:
        n = len(matrix_entries)

        if n == 0:
            raise ValueError

        A = []

        for row_entries in matrix_entries:

            row = []

            for entry in row_entries:

                value = float(entry.get())

                if value.is_integer():
                    value = int(value)

                row.append(value)

            A.append(row)

        d = det(A)

        determinant_label.config(
            text=f"Determinant = {round(d, 10)}"
        )

        inv1 = inverse_det(A)
        inv2 = inverse_gj(A)

        if inv1 is None or inv2 is None:

            determinant_result.delete("1.0", tk.END)
            gauss_result.delete("1.0", tk.END)

            determinant_result.insert(
                tk.END,
                "Inverse does not exist."
            )

            gauss_result.insert(
                tk.END,
                "Inverse does not exist."
            )

            comparison_label.config(
                text="No inverse exists."
            )

            verification_label.config(
                text=""
            )

            return

        determinant_result.delete("1.0", tk.END)
        determinant_result.insert(
            tk.END,
            format_matrix(inv1)
        )

        gauss_result.delete("1.0", tk.END)
        gauss_result.insert(
            tk.END,
            format_matrix(inv2)
        )

        same = all(
            abs(inv1[i][j] - inv2[i][j]) < 1e-8
            for i in range(n)
            for j in range(n)
        )

        if same:
            comparison_label.config(
                text="✓ The two results are identical."
            )
        else:
            comparison_label.config(
                text="✗ The two results are different."
            )

        if verify_inverse(A, inv2):

            verification_label.config(
                text="✓ Verification successful: A × A^-1 = I"
            )

        else:

            verification_label.config(
                text="✗ Verification failed."
            )

    except ValueError:

        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers in all matrix fields."
        )


# Explanation:
# This function connects the GUI with the mathematical
# functions.
#
# It reads the matrix entered by the user,
# calculates the determinant,
# calculates the inverse using both methods,
# compares the two results,
# and verifies the inverse.
#
# All results are then displayed in the GUI.


# Main GUI Window

window = tk.Tk()

window.title("Inverse Matrix Calculator")

window.geometry("850x850")

window.resizable(False, False)


# Title

title_label = tk.Label(
    window,
    text="INVERSE MATRIX CALCULATOR",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=15)


# Matrix Size

size_frame = tk.Frame(window)

size_frame.pack(pady=5)

size_label = tk.Label(
    size_frame,
    text="Matrix Size (n):",
    font=("Arial", 12)
)

size_label.pack(side="left", padx=5)

size_entry = tk.Entry(
    size_frame,
    width=8,
    justify="center"
)

size_entry.pack(side="left", padx=5)

create_button = tk.Button(
    size_frame,
    text="Create Matrix",
    command=create_matrix,
    width=15
)

create_button.pack(side="left", padx=5)


# Matrix Input Area

input_label = tk.Label(
    window,
    text="Enter Matrix:",
    font=("Arial", 13, "bold")
)

input_label.pack(pady=10)

matrix_frame = tk.Frame(window)

matrix_frame.pack(pady=5)

matrix_entries = []


# Calculate Button

calculate_button = tk.Button(
    window,
    text="Calculate Inverse",
    command=calculate,
    font=("Arial", 12, "bold"),
    width=20,
    height=2
)

calculate_button.pack(pady=15)


# Determinant Result

determinant_label = tk.Label(
    window,
    text="Determinant =",
    font=("Arial", 12, "bold")
)

determinant_label.pack(pady=5)


# Determinant Method Result

method1_label = tk.Label(
    window,
    text="Determinant Method",
    font=("Arial", 12, "bold")
)

method1_label.pack(pady=5)

determinant_result = tk.Text(
    window,
    width=45,
    height=5,
    font=("Courier New", 11)
)

determinant_result.pack()


# Gauss-Jordan Result

method2_label = tk.Label(
    window,
    text="Gauss-Jordan Method",
    font=("Arial", 12, "bold")
)

method2_label.pack(pady=5)

gauss_result = tk.Text(
    window,
    width=45,
    height=5,
    font=("Courier New", 11)
)

gauss_result.pack()


# Comparison Result

comparison_label = tk.Label(
    window,
    text="",
    font=("Arial", 12, "bold")
)

comparison_label.pack(pady=10)


# Verification Result

verification_label = tk.Label(
    window,
    text="",
    font=("Arial", 12, "bold")
)

verification_label.pack(pady=5)


# Explanation:
# Tkinter is used to create the graphical user interface.
#
# The GUI contains:
#
# 1. Matrix size input
# 2. Matrix input fields
# 3. Create Matrix button
# 4. Calculate Inverse button
# 5. Determinant result
# 6. Determinant Method result
# 7. Gauss-Jordan Method result
# 8. Comparison result
# 9. Verification result
#
# The main window is created first, and all GUI
# components are placed inside it.
#
# Finally, mainloop() keeps the window running.


window.mainloop()