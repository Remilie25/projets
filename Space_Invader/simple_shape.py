#HEADER
# Description : The famous space invader implemented with tkinter, here is the definition of the class named simple_shape
# Date : 11/12/23
# Authors : De Pretto Remi, Aussant Esteban
# TO DO : add more parameters with fun

class Simple_shape:
    def __init__(self, width, height, shape, color, border_color, margins = [0, 0, 0, 0]):
        assert shape in ['r', 'o', 'i'] #'r' for rectangle, 'o' for oval and 'i' for image
        self.__width = width
        self.__height = height
        self.__shape = shape
        self.__margins = margins
        self.__color = color
        self.__border_color = border_color
    
    def width(self):
        return self.__width
    
    def height(self):
        return self.__height

    def shape(self):
        return self.__shape
    
    def margin_top(self):
        return self.__margins[0]
    
    def margin_left(self):
        return self.__margins[1]
    
    def margin_right(self):
        return self.__margins[2]
    
    def margin_bottom(self):
        return self.__margins[3]
    
    def color(self):
        return self.__color
    
    def border_color(self):
        return self.__border_color