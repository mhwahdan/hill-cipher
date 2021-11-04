# This is a module for implementing hill cipher Algorithm
from math import sqrt
from matrixhandler import ModularMatrixHandler


class HillCipher:
    def __init__(self, key):
        self.matrixHandler = ModularMatrixHandler(27)
        key = key.replace(" ", "[")
        if not (sqrt(len(key)).is_integer()):
            raise Exception("This string cannot be used as cipher as its length must have a perfect square root")
        self.__complexity = int(sqrt(len(key)))
        self.__key = self.__generate_key(key)
        if self.matrixHandler.has_multiplicative_inverse(self.__key):
            self.__inverse_key = self.__generate_inverse_key()
        else:
            raise Exception("Key is invalid as its determinant does not have a 16 modular multiplicative inverse")
        return

    def __generate_key(self, string):
        characters = list(string)
        integers = [(ord(c.upper()) - 65) for c in list(characters)]
        for x in integers:
            if self.matrixHandler.check_number(x):
                raise Exception("Only characters from a - z or A - Z or spaces are allowed")
        matrix = ModularMatrixHandler.generate(self.__complexity, self.__complexity)
        iterator = 0
        for row in range(self.__complexity):
            for column in range(self.__complexity):
                matrix[row][column] = integers[iterator]
                iterator += 1
        return matrix

    def __generate_inverse_key(self):
        determinant = self.matrixHandler.determinant(self.__key)
        determinant = self.matrixHandler.adjust_number(determinant)
        transpose = self.matrixHandler.matrix_cofactor(self.__key)
        mul_inverse = self.matrixHandler.find_multiplicative_inverse(determinant)
        temp = mul_inverse * transpose
        output = ModularMatrixHandler.generate(self.__complexity, self.__complexity)
        for i in range(self.__complexity):
            for j in range(self.__complexity):
                output[i][j] = self.matrixHandler.adjust_number(int(temp[i][j]) + (1 if temp[i][j] >= 0 else -1))
        return output

    def __generate_substring_matrices(self, string):
        string = list(string.replace(" ", "["))
        string = [x.upper() for x in string]
        while True:
            if len(string) % self.__complexity == 0:
                break
            string = string + ["["]
        strings = [string[i:i+self.__complexity] for i in range(0, len(string), self.__complexity)]
        matrices = []
        for x in strings:
            matrices.append(
                ModularMatrixHandler.generate(self.__complexity, 1)
            )
            for y in range(self.__complexity):
                matrices[-1][y][0] = ord(x[y]) - 65
        return matrices

    def __operate(self, text, key):
        matrices = self.__generate_substring_matrices(text)
        ciphers = []
        for x in matrices:
            ciphers.append(ModularMatrixHandler.multiply(key, x))
        x = len(ciphers)
        for i in range(x):
            for j in range(len(ciphers[i])):
                ciphers[i][j] = self.matrixHandler.adjust_number(ciphers[i][j])
        result = ""
        for x in ciphers:
            for y in x:
                result += chr(int(y[0]) + 65)
        return result

    def encrypt(self, text):
        return self.__operate(text, self.__key)

    def decrypt(self, cipher):
        string = self.__operate(cipher, self.__inverse_key).replace("[", " ").lower()
        string = string[::-1]
        counter = 0
        for x in string:
            if x != " ":
                break
            counter += 1
        string = string[counter::]
        return string[::-1]


if __name__ == "__main__":
    _cipher = HillCipher("hill")
    print(_cipher.encrypt("retreat now"))  # expected output ==> QP[SBRRJOALP
    print(_cipher.decrypt("QP[SBRRJOALP"))
