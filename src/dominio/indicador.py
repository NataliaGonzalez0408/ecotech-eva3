# dominio/indicador.py · extracto del constructor
class Indicador:
    def __init__(self, fecha, valor, verificado_en=None,
                    fuente="api_dolar_curso"):
# Validar fecha ISO y valor numérico finito positivo.
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en


