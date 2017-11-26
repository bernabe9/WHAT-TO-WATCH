from util import inicializar_algoritmo

class Clasificador:
    def __init__(self):
        self.entrenar()

    def entrenar(self):
        # Prepara el algoritmo
        (algo, testset) = inicializar_algoritmo()
        self.algo = algo
        self.testset = testset
