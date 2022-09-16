class ComidaRest:
    def __init__(self,name,price,quantity,type,packing):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.type = type
        self.packing = packing

    def show_attr(self):
        return f"""
        Nombre: {self.name}
        Precio: {self.price}
        Cantidad: {self.quantity}
        Tipo: {self.type}
        Packing: {self.packing}"""

