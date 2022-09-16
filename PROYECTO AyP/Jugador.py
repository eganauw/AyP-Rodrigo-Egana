class Jugador:
    def __init__(self,playername,number,position):
        self.playername = playername
        self.number = number
        self.position = position

    def show_attr(self):
        return f"""Nombre del jugador: {self.playername}
        Numero: {self.number}
        Posición: {self.position}
        """