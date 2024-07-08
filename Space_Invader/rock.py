class Rock:
    
    def __init__(self):
        self.__number_rock_line = 2
        self.__number_rock_colum = 3

    def number_rock_colum(self):
        return self.__number_rock_colum

    def number_rock_line(self):
        return self.__number_rock_line 
    
    def create_rock(self, line, colum):
        return True

class Big(Rock):

    def __init__(self):
        self.__number_rock_line = 3
        self.__number_rock_colum = 4
        
    def number_rock_colum(self):
        return self.__number_rock_colum

    def number_rock_line(self):
        return self.__number_rock_line
    
    def create_rock(self, line, colum):
        return True


class Donut(Rock):

    def __init__(self):
        self.__number_rock_line = 3
        self.__number_rock_colum = 3
        
    def number_rock_colum(self):
        return self.__number_rock_colum

    def number_rock_line(self):
        return self.__number_rock_line 
    
    def create_rock(self, line, colum):
        if line == 1 and colum == 1:
            return False
        return True


class Triangle(Rock):

    def __init__(self):
        self.__number_rock_line = 3
        self.__number_rock_colum = 5
        

    def number_rock_colum(self):
        return self.__number_rock_colum

    def number_rock_line(self):
        return self.__number_rock_line 
    
    def create_rock(self, line, colum):
        if line == 0 and colum == 2 : 
            return True
        if line == 1 and colum in [1, 2, 3]:
            return True
        if line == 2:
            return True
        return False