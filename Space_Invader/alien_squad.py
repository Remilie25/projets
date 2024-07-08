#HEADER
# Description : The famous space invader implemented with tkinter
# Date : 20/11/23
# Authors : De Pretto Remi, Aussant Esteban
# TO DO : call optimise on kills

##Import
import alien #pas utile

##Class def

class Alien_squad:
    def __init__(self, n, p):
        self.__x_speed = 1
        self.__y_speed = 2
        self.__width = 60 * p - 10
        self.__height = 30 * n - 10
        self.__x = 0
        self.__y = 0
        self.__x_limit = 1000
        self.__y_limit = 1000
        self.__n = n
        self.__p = p
        self.__mapping = [[False]* p for _ in range(n)]
        self.__alien_to_pos = {}
    
    def add(self, alien, x_pos, y_pos):
        assert 0 <= x_pos < self.__p and 0 <= y_pos < self.__n, "The position of the new alien is beyond the squad limit."
        assert not(self.__mapping[y_pos][x_pos]), "The position given is already occupied."
        self.__mapping[y_pos][x_pos] = True
        self.__alien_to_pos[alien] = (y_pos, x_pos)
    
    def optimise(self):
        '''No inputs nor outputs. This method optimises the dimension of the self.__mapping and self.__alien_to_pos to be 
        the littlest matrixes with no empty borders (ie with at least one alien one each border).'''
        rm_1st_l = True
        rm_last_l = True
        rm_1st_c = True
        rm_last_c = True
        i = 0

        while (rm_1st_l or rm_last_l) and i < self.__p:
            if self.__mapping[0][i]:
                rm_1st_l = False
            if self.__mapping[self.__n - 1][i]:
                rm_last_l = False
            i += 1
        
        i = 0

        while (rm_1st_c or rm_last_c) and i < self.__n:
            if self.__mapping[i][0]:
                rm_1st_c = False
            if self.__mapping[i][self.__p -1]:
                rm_last_c = False
            i += 1

        if rm_1st_l:
            self.__mapping = self.__mapping[1:]
            self.__n -= 1
            self.__height = 30 * self.__n - 10      #Same as taking away 30.
            self.__y += 30

            for alien in self.__alien_to_pos.keys():
                y, x = self.__alien_to_pos[alien]
                self.__alien_to_pos[alien] = (y - 1, x)
        
        if rm_last_l:
            self.__mapping = self.__mapping[:-1]
            self.__n -= 1
            self.__height = 30 * self.__n - 10
            self.allows_to_shoot()
        
        if rm_1st_c:
            for i in range(self.__n):
                self.__mapping[i] = self.__mapping[i][1:]
            self.__p -= 1
            self.__width = 60 * self.__p - 10       #Same as taking away 60.
            self.__x += 60

            for alien in self.__alien_to_pos.keys():
                y, x = self.__alien_to_pos[alien]
                self.__alien_to_pos[alien] = (y, x - 1)
        
        if rm_last_c:
            for i in range(self.__n):
                self.__mapping[i].pop()
            self.__p -= 1
            self.__width = 60 * self.__p - 10

        if (rm_1st_l or rm_last_l or rm_1st_c or rm_last_c) and not(rm_1st_l and rm_last_l and rm_1st_c and rm_last_c):
            self.optimise()

    
    def moves(self):
        if self.__x + self.__width + self.__x_speed >= self.__x_limit:
            delta_x = self.__x_limit - self.__width - self.__x

            for alien in self.__alien_to_pos.keys():
                alien.h_moves(delta_x)

            self.__x_speed *= -1
            self.__x += delta_x

        elif self.__x + self.__x_speed <= 0:
            if self.__y + self.__height + self.__y_speed > self.__y_limit:
                delta_y = self.__y_limit - self.__height - self.__y

                for alien in self.__alien_to_pos.keys():
                    alien.v_moves(delta_y)

                self.__y += delta_y

            else:
                for alien in self.__alien_to_pos.keys():
                    alien.h_moves(-1 * self.__x)
                    alien.v_moves()
                self.__x = 0
                self.__x_speed *= -1
                self.__y += self.__y_speed
                if self.__y + self.__height > self.__y_limit:
                    self.__y = self.__y_limit - self.__height
        else:
            self.__x += self.__x_speed

            for alien in self.__alien_to_pos.keys():
                alien.h_moves(self.__x_speed)
    
    def dies(self, alien):
        pos_cople = self.__alien_to_pos[alien]
        self.__mapping[pos_cople[0]][pos_cople[1]] = False
        del self.__alien_to_pos[alien]
        self.optimise()

    def allows_to_shoot(self):
        for alien in self.__alien_to_pos.keys():
            if self.__alien_to_pos[alien][0] == self.__n - 1:
                alien.allowed_to_shoot()

    def mapping(self):
        return self.__mapping
    
    def n(self):
        return self.__n
    
    def p(self):
        return self.__p