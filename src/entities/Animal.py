# Criação classe Status
class Status:
    def __init__(self, alisau, energia, felicidade, resistencia, forca):
        self.alisau = alisau
        self.energia = energia
        self.felicidade = felicidade
        self.resistencia = resistencia
        self.forca = forca

    def getStatus(self):
        return {
            "Alimentacao Saudável": self.alisau,
            "energia": self.energia,
            "felicidade": self.felicidade,
            "resistencia": self.resistencia,
            "forca": self.forca
        }

    # Método para atualizar status
    def atualizarStatus(self, outro_status):
        self.alisau += outro_status.alisau
        self.energia += outro_status.energia
        self.felicidade += outro_status.felicidade
        self.resistencia += outro_status.resistencia
        self.forca += outro_status.forca

# Criação animal
class Animal:
    def __init__(self, id, nome, status):
        self.id = id
        self.nome = nome
        self.status = status

    def getAlimento(self):
        return self.status.getAlimentacao()

    def getStatus(self):
        return self.status.getStatus()

    def getNome(self):
        return self.nome

# Teste de uso
status_cenoura = Status(10, 10, -5, 5, 5)
status_animal = Status(50, 50, 50, 50, 50)
bicho1 = Animal(1, "baat", status_animal)
print(f"O animal, {bicho1.getNome()} tem os seguintes status: {bicho1.getStatus()}")

status_animal.atualizarStatus(status_cenoura)
print(f"O animal {bicho1.getNome()}, agora tem o os status {bicho1.getStatus()}")
