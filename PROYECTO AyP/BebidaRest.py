class BebidaRest:
    def __init__(self,name,price,quantity,type,alcoholic):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.type = type
        self.alcoholic = alcoholic

    def show_attr(self):
        return f"""
        Nombre: {self.name}
        Precio: {self.price}
        Cantidad: {self.quantity}
        Tipo: {self.type}
        Alcoholica: {self.alcoholic}"""
