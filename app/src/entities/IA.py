class IA:
    def __init__(self, alimento, listaAlimento):
        self.alimento = alimento
        self.listaAlimento = []
    
    def checkALimento (alimento, listaAlimento):
        if alimento in listaAlimento:
            print(f"O alimento {alimento} está presente na lista de alimentos")
        if alimento not in listaAlimento:
            print(f"{alimento} não encontrado na lista de alimentos")

    def adicionaAlimento(alimento, listaAlimento):
        listaAlimento.append(alimento)
        print(f"{alimento} adicionado a lista de alimentos")

    #criar send alimento quando tiver conexão com o banco e ia
        