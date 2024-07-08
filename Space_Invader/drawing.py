#HEADER
# Description : The famous space invader implemented with tkinter, here is the definition of the class named drawing
# Date : 14/12/23
# Authors : De Pretto Remi, Aussant Esteban
# TO DO :

class drawing:
    def __init__(self, x_pos, y_pos, drawings_array):
        nbr_types = [int, float]
        assert type(x_pos) in nbr_types, "x_pos must be a number."
        assert type(y_pos) in nbr_types, "y_pos must be a number."
        assert type(drawings_array) == list, "drawings_array must be an int array (the integers represents the id of a drawing in canvas)."
        
        self.__x = x_pos
        self.__y = y_pos
        self.__drawings_array = drawings_array

    def x(self):
        return self.__x

    def y(self):
        return self.__y
    
    def set_coords(self, x, y):
        self.__x = x
        self.__y = y
    
    def drawings(self):
        return self.__drawings_array