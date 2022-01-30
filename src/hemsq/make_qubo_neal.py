
# amplify でマシンに渡していた多項式 Q を行列形式に変換
def poly_to_dict(Q):
    Q_matrix = Q.to_Matrix()[0]
    matrix_size = Q_matrix.size()
    Q_sa = {}
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i >= j:
                if Q_matrix[i, j] != 0:
                    Q_sa[(i, j)] = Q_matrix[i, j]
    return Q_sa
