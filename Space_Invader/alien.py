#HEADER
# Description : The famous space invader implemented with tkinter
# Date : 13/11/23
# Authors : De Pretto Remi, Aussant Esteban
# TO DO : move with squad_alien

#Import
from random import randint

#Def of the Alien class

class Alien:
    def __init__(self, x, y):
        self.__y_speed = 20
        self.__width = 50
        self.__height = 20
        self.__x = 60 * x
        self.__y = 30 * y
        self.__x_limit = 1000
        self.__y_limit = 1000
        self.__alive = True
        self.__life = 1
        self.__is_allowed_shoot = False
    
    def x(self):
        return self.__x
    
    def y(self):
        return self.__y
    
    def width(self):
        return self.__width
    
    def height(self):
        return self.__height
    
    def pg_width(self):
        return self.__x_limit
    
    def pg_height(self):
        return self.__y_limit
    
    def is_alive(self):
        return self.__alive

    def h_moves(self, delta_x):
        self.__x += delta_x
    
    def v_moves(self):
        self.__y += self.__y_speed
    
    def hits(self):
        self.__life -= 1
        if self.__life <= 0:
            self.__alive = False
    
    def is_allowed_shoot(self):
        return self.__is_allowed_shoot
    
    def allowed_to_shoot(self):
        if type(self) == Shooter:
            self._Alien__is_allowed_shoot = True
    
    def standardized_type(self):
        return 'Alien'

class Warior(Alien):
    def __init__(self):
        print('TO DO')


class Shooter(Alien):    
    def shoots(self):
        if randint(0, 500) == 0:
            return True
        return False
    
    def standardized_type(self):
        return 'Shooter'