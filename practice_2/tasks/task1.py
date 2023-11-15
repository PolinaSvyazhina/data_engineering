import numpy as np
import json

matrix = np.load("../data/matrix_5.npy")
matrix = matrix.astype('float')

size = len(matrix)

matrix_stat = dict()
matrix_stat['sum'] = np.sum(matrix)
matrix_stat['avr'] = matrix_stat['sum'] / (size * size)
matrix_stat['sumMD'] = np.trace(matrix)
matrix_stat['avrMD'] = matrix_stat['sumMD'] / matrix.shape[0]
matrix_stat['sumSD'] = 0
matrix_stat['avrSD'] = 0
matrix_stat['max'] = matrix.max()
matrix_stat['min'] = matrix.min()

for i in range(0, size):
    for j in range(0, size):
        if i + j == (size - 1):
            matrix_stat['sumSD'] += matrix[i][j]

matrix_stat['avrSD'] = matrix_stat['sumSD'] / size

with open('../result/task1/matrix_stat.json', 'w') as result:
    result.write(json.dumps(matrix_stat))

norm_matrix = np.ndarray((size, size), dtype=float)

for i in range(0, size):
    for j in range(0, size):
        norm_matrix[i][j] = matrix[i][j] / matrix_stat['sum']

np.save("../result/task1/norm_matrix.npy", norm_matrix)
