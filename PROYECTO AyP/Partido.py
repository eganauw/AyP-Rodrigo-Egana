from Equipo import Equipo
class Partido:
    def __init__(self,equipo1,equipo2,estadio,arbitro,asientos_ocupados):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.estadio = estadio
        self.arbitro = arbitro
        self.asientos_ocupados = asientos_ocupados


    def show_attr(self):
        return f"""{self.equipo1.name} vs {self.equipo2.name}
        Lugar: {self.estadio.stadiumname}
        Árbitro: {self.arbitro}
        """

    def getAsientosocupados(self):
        return self.asientos_ocupados


    
