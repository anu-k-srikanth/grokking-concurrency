


# [1,2,3] x [7,8] =  [1*7+2*9+3*11,1*8+2*10+3*12]
# [4,5,6]   [9,10]   [0,0]
#           [11,12]

from multiprocessing import Pool
import random


def multiply_matrices(matrix_a, matrix_b):
    num_rows_a, num_cols_a = len(matrix_a), len(matrix_a[0])
    num_rows_b, num_cols_b = len(matrix_b), len(matrix_b[0])

    if num_cols_a != num_rows_b:
        raise ArithmeticError(f"matrix_a {matrix_a} and matrix_b {matrix_b} cannot be multiplied")

    sol_matrix = [[0 for _ in range(num_cols_b)] for _ in range(num_rows_a)]

    for i in range(num_rows_a):
        for j in range(num_cols_b):
            for k in range(num_cols_a):
                sol_matrix[i][j] += matrix_a[i][k] * matrix_b[k][j]
    
    return sol_matrix

def process_row(args: tuple):
    matrix_a, matrix_b, row_idx = args
    sol = [0 for _ in range(len(matrix_b[0]))]

    num_rows_a, num_cols_a = len(matrix_a), len(matrix_a[0])
    num_rows_b, num_cols_b = len(matrix_b), len(matrix_b[0])

    for j in range(num_cols_b):
        for k in range(num_cols_a):
            sol[j] += matrix_a[row_idx][k] * matrix_b[k][j]
    
    return sol

def multiply_matrices_concurrent(matrix_a, matrix_b):
    num_rows_a, num_cols_a = len(matrix_a), len(matrix_a[0])
    num_rows_b, num_cols_b = len(matrix_b), len(matrix_b[0])
    
    pool = Pool()
    results = pool.map(process_row, [(matrix_a, matrix_b, i) for i in range(num_rows_a)])
    pool.close()
    pool.join()

    return results

if __name__ == "__main__":
    rows, cols = 3, 4 
    matrix_a = [[random.randint(0,9) for _ in range(cols)] for _ in range(rows)]
    matrix_b = [[random.randint(0,9) for _ in range(rows)] for _ in range(cols)]

    print(f"matrix_a: {matrix_a}")
    print(f"matrix_b: {matrix_b}")

    print(f"product: " + str(multiply_matrices(matrix_a, matrix_b)))
    print(f"product - concurrent: " + str(multiply_matrices_concurrent(matrix_a, matrix_b)))


# Strategies for Concurrency: 
# 1. How can we break this problem into separate parts that are not interdependent
    # -> Every cel is calculated from a particular row and column of the matrix so we could divide this into 
    #    the same number of problems as the number of cells in the resulting solution matrix 
    #        -> We would need to duplicate the input across various parts
    #        -> We might not have enough processing units to be able to decompose into so many tasks 