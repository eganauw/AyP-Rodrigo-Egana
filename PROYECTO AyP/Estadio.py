class Estadio:
    def __init__(self,stadiumname,generalmap,vipmap):
        self.stadiumname = stadiumname
        self.generalmap = generalmap
        self.vipmap = vipmap
    
    def show_attr(self):
        return f"""Nombre del estadio: {self.stadiumname}
        Mapa General: {self.generalmap}
        Mapa VIP: {self.vipmap}
        """