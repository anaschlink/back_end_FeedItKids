class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.animal_estimacao = None
        self.objetivos = []

    # criar deleteuser quando tiver a conexao com o banco
        
    def chooseAnimalEstimacao(self, animal):
        self.animal_estimacao = animal
        print(f"Animal de estimação escolhido: {animal.getNome()}")

    # criar send alimento quando tiver a conexao com o banco
        
    def getObjetivos(self):
        return self.objetivos
    
    # criar completeobjetivos quando tiver a conexao com o banco

