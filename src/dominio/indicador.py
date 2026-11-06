class Indicador:
    def __init__(self, fecha, valor, verificado_en=None, fuente="api_dolar_curso"):
        # Validar fecha ISO y valor numérico finito positivo.
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en

    def __str__(self) -> str:
        return f"{self.valor} {self.unidad} (Fecha: {self.fecha})"

    def __repr__(self) -> str:
        return self.__str__()