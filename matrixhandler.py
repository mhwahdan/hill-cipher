import numpy as np

class ModularMatrixHandler:
    def __init__(self, modulus):
        self.modulus = modulus

    def adjust_number(self, number):
        if number > 0:
            return int(number) % self.modulus
        else:
            if number < -1 * self.modulus:
                return int(number + (int((abs(number) / self.modulus)) + 1) * self.modulus)
            else:
                return self.modulus + int(number)

    def check_number(self, number):
        return number < 0 or number > self.modulus

    def find_multiplicative_inverse(self, determinant):
        for i in range(self.modulus):
            if (i * determinant) % self.modulus == 1:
                return i
        raise Exception("cannot find multiplicative inverse for the number " + str(determinant))

    def has_multiplicative_inverse(self, matrix):
        determinant = self.determinant(matrix)
        for i in range(self.modulus):
            if (i * determinant) % self.modulus == 1:
                return True
        return False

    def determinant(self, matrix):
        determinant = np.linalg.det(matrix)
        return self.adjust_number(determinant)

    @staticmethod
    def matrix_cofactor(matrix):
        # return cofactor matrix of the given matrix
        matrix = np.transpose(matrix)
        return np.linalg.inv(matrix).T * np.linalg.det(matrix)

    @staticmethod
    def multiply(matrix1, matrix2):
        return np.matmul(matrix1, matrix2)

    @staticmethod
    def generate(rows, columns):
        return np.zeros(
            (rows, columns),
            dtype=np.int32
        )