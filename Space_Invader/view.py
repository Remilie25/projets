#HEADER
# Description : The famous space invader implemented with tkinter, here is the definition of the class named view
# Date : 11/12/23
# Authors : De Pretto Remi, Aussant Esteban
# TO DO :

class View:
    def __init__(self, width, height, structure, interline):
        nbr_types = [int, float]
        assert type(width) in nbr_types, "The parameter width must be an number."
        assert type(height) in nbr_types, "The parameter height must be an number."
        assert (type(interline) in nbr_types) or (type(interline) == list and 
            len(interline) == len(structure)), "The parameter interline must be an number or an array of len(structure) - 1 numbers."
        
        self.__width = width
        self.__height = height
        self.__structure = structure
        self.__interline = interline
    
    def width(self):
        return self.__width
    
    def height(self):
        return self.__height

    def structure(self):
        return self.__structure
    
    def interline(self, i = 0):
        if type(self.__interline) == list:
            return self.__interline[i]
        else:
            return self.__interline