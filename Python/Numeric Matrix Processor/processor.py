import numpy


def read_matrix_shape():
    return [int(d) for d in input().split()]


def read_matrix(shape):
    return [[float(el) for el in input().split()] for _ in range(shape[0])]


def sum_matrix(m1, m2):
    return [[m1[row][col] + m2[row][col] for col in range(len(m1[0]))] for row in range(len(m1))]


def mul_matrix_const(m, c):
    return [[m[row][col] * c for col in range(len(m[0]))] for row in range(len(m))]


def transpose(m, line=1):  # line: 1-main diagonal, 2-side diagonal, 3-vertical line, 4-horizontal line
    return [[m[row][col] for row in range(len(m))] for col in range(len(m[0]))] if line == 1 else \
           [[m[row][col] for row in range(-1, -len(m) - 1, -1)] for col in range(-1, -len(m[0]) - 1, -1)] \
               if line == 2 else \
           [m[row][::-1] for row in range(len(m))] if line == 3 else \
           [m[row] for row in range(-1, -len(m) - 1, -1)]  # line == 4


def mul_matrix_matrix(m1, m2):
    m2_t = transpose(m2)
    return [map(sum, [[m1[row1][col] * m2_t[row2][col] for col in range(len(m1[0]))]
            for row2 in range(len(m2_t))]) for row1 in range(len(m1))]


def determinant(m):
    return numpy.linalg.det(m)


def inverse(m):
    return numpy.linalg.inv(m)


def print_matrix(m):
    for row in m:
        print(f'{" ".join(map(str, row))}')


if __name__ == "__main__":
    while True:
        menu = input('1. Add matrices\n2. Multiply matrix by a constant\n'
                     '3. Multiply matrices\n4. Transpose matrix\n5. Calculate a determinant\n'
                     '6. Inverse matrix\n0. Exit\nYour choice: ')
        if menu == '1':
            print('Enter size of first matrix:', end=' ')
            mx1_size = read_matrix_shape()
            print('Enter first matrix:')
            mx1 = read_matrix(mx1_size)
            print('Enter size of second matrix:', end=' ')
            mx2_size = read_matrix_shape()
            print('Enter second matrix:')
            mx2 = read_matrix(mx2_size)
            if mx1_size != mx2_size:
                print('The operation cannot be performed.')
            else:
                print('The result is:')
                print_matrix(sum_matrix(mx1, mx2))
        elif menu == '2':
            print('Enter size of matrix:', end=' ')
            mx_size = read_matrix_shape()
            print('Enter matrix:')
            mx = read_matrix(mx_size)
            const = float(input('Enter constant: '))
            print('The result is:')
            print_matrix(mul_matrix_const(mx, const))
        elif menu == '3':
            print('Enter size of first matrix:', end=' ')
            mx1_size = read_matrix_shape()
            print('Enter first matrix:')
            mx1 = read_matrix(mx1_size)
            print('Enter size of second matrix:', end=' ')
            mx2_size = read_matrix_shape()
            print('Enter second matrix:')
            mx2 = read_matrix(mx2_size)
            if mx1_size[1] != mx2_size[0]:
                print('The operation cannot be performed.')
            else:
                print('The result is:')
                print_matrix(mul_matrix_matrix(mx1, mx2))
        elif menu == '4':
            menu_tr = input('1. Main diagonal\n2. Side diagonal\n'
                            '3. Vertical line\n4. Horizontal line\nYour choice: ')
            print('Enter matrix size:', end=' ')
            mx_size = read_matrix_shape()
            print('Enter matrix:')
            mx = read_matrix(mx_size)
            print('The result is:')
            print_matrix(transpose(mx, int(menu_tr)))
        elif menu == '5':
            print('Enter matrix size:', end=' ')
            mx_size = read_matrix_shape()
            print('Enter matrix:')
            mx = read_matrix(mx_size)
            print('The result is:')
            print(determinant(mx), '\n')
        elif menu == '6':
            print('Enter matrix size:', end=' ')
            mx_size = read_matrix_shape()
            print('Enter matrix:')
            mx = read_matrix(mx_size)
            print('The result is:')
            print_matrix(inverse(mx))
        else:
            break
