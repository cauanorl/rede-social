class SeiLa:
    parede = 'as'


valor = SeiLa()

print(getattr(valor, 'parede', False))


