#HEADER
# Description : The famous space invader implemented with tkinter
# Date : 20/11/23
# Authors : De Pretto Remi, Aussant Esteban
# TO DO : create types of ammunitions

class Ammunition:
    def __init__(self, x, y, direction):
        self.__width = 10
        self.__height = 20
        self.__x = x
        self.__y = y
        self.__y_speed = direction
        self.__blown_up = False
        self.__y_limit = 1000
    
    def is_blown_up(self):
        return self.__blown_up
    
    def hits(self):
        self.__blown_up = True

    def moves(self):
        self.__y += self.__y_speed
        if self.__y + self.__width >= self.__y_limit:
            self.__blown_up = True
            self.__y >= self.__y_limit - self.__width
        elif self.__y <= 0:
            self.__blown_up = True
            self.__y = 0
    
    def x(self):
        return self.__x
    
    def y(self):
        return self.__y
    
    def width(self):
        return self.__width
    
    def height(self):
        return self.__height

    def standardized_type(self):
        return 'Ammunition'
