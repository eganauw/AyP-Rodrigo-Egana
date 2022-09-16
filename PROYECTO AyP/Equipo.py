class Equipo:
    def __init__(self,name,stadium,lineup,stats):
        self.name = name
        self.stadium = stadium
        self.lineup = lineup
        self.stats = stats

    def getGoalkeeper(self):
        for i in self.lineup:
            if i.position == "Goalkeeper":
                return i

    def getPoints(self):
        return self.stats["Puntos"]

    def getName(self):
        return self.name

    def show_attr(self):
        return f"""
        Nombre: {self.name}
        {self.stadium.show_attr()}
        {self.lineup[0].show_attr()}
        {self.lineup[1].show_attr()}
        {self.lineup[2].show_attr()}
        {self.lineup[3].show_attr()}
        {self.lineup[4].show_attr()}
        {self.lineup[5].show_attr()}
        {self.lineup[6].show_attr()}
        {self.lineup[7].show_attr()}
        {self.lineup[8].show_attr()}
        {self.lineup[9].show_attr()}
        {self.lineup[10].show_attr()}
        """





