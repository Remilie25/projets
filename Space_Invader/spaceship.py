#HEADER
# Description : The famous space invader implemented with tkinter
# Date : 13/11/23
# Authors : De Pretto Remi, Aussant Esteban
# TO DO : all

class Spaceship: 
    def __init__(self, name, life, x_start, y_start):
        self.__name = name
        self.__life = life
        self.__x = x_start
        self.__y = y_start
        self.__speed  = 3
        self.__width = 100
        self.__height = 50
        self.__x_max = 1000
        self.__alive = True

    def x(self):
        return self.__x
    
    def y(self):
        return self.__y
    
    def width(self):
        return self.__width
    
    def height(self):
        return self.__height
    
    def life(self):
         return self.__life
    
    def move(self, direction):
        if direction :
            if self.__x < self.__x_max - self.__width  :
                    self.__x += self.__speed

        else :           
            if self.__x > 0 :
                    self.__x -= self.__speed

    def hits(self):
        self.__life -= 1
        if self.__life <= 0:
            self.__alive = False
    
    def standardized_type(self):
        return 'Spaceship'

    def is_alive(self):
         return self.__alive