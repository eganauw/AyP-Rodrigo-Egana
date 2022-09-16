from Partido import Partido
class ResultadoPartido(Partido):
    def __init__(self,equipo1,equipo2,estadio,arbitro,asientos_ocupados,resultado):
        Partido.__init__(self,equipo1,equipo2,estadio,arbitro,asientos_ocupados)
        self.resultado = resultado


    def show_attr(self):
        return f"""{Partido.show_attr(self)}
        Resultado: 
        {self.resultado["Equipo local"]}: {self.resultado["Goles equipo1"]}-{self.resultado["Goles equipo2"]} :{self.resultado["Equipo visitante"]}
        {self.resultado["formatg1"]}: {self.resultado["goleadoreslocal"]}
        {self.resultado["formatg2"]}: {self.resultado["goleadoresvisitante"]}
        
        """
