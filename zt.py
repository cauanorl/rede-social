class al:
    def __init__(self):
        self._name = "Senha"
    
    @property
    def name(self):
        return "Nome oculto"
    
    @name.setter
    def name(self, new_name):
        self._name = new_name


algo = al()

algo.name = 'Name is anonymous'
print(algo.name)
