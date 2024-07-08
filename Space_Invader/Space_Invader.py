# HEADER
# Description : The famous space invader implemented with tkinter
# Date : 13/11/23
# Authors : De Pretto Remi, Aussant Esteban
#TO DO : bonus, pile -> magazines, keep alien squad data ?,
#diff type of ammo + freq, 
#Infinite waves, menu + keybindings + rules + highscore, end of the game, draw -> add more shapes

##Emergency : pile, infinite waves, boss, menu, rocks, doc, shapes?

##Imports
import alien
import alien_squad
import ammunition
import view
import simple_shape
import drawing
from queue import Queue
from tkinter import Tk,Label,StringVar,Entry,Button,Canvas,messagebox, Frame
import spaceship
import rock
from random import randint

##Functions
def dictio_max_key(dictio):
        '''Input : a dictionary with couples of int for the keys.
        Output : a couple of the max of the first components and the max of the second components.'''

        x_max_temp, y_max_temp = -1 * float('Inf'), -1 * float('Inf')

        for couple in dictio.keys():
            if couple[0] > x_max_temp:
                x_max_temp = couple[0]
            if couple[1] > y_max_temp:
                y_max_temp = couple[1]
        
        return x_max_temp, y_max_temp

cache = []

#Class def
class Space_invader:
    def __init__(self):
        self.__is_game_on = False
        self.__game_id = 0

        alien_init = alien.Alien(0, 0)
        self.__Alien_w = alien_init.pg_width()
        self.__Alien_h = alien_init.pg_height()
        del alien_init

        ammo_init = ammunition.Ammunition(0, 0, 1)
        self.__Ammo_height = ammo_init.height()
        del ammo_init


        self.__alien_queue = Queue()        #Keeps alien drawings to refresh 
        self.__ammo_queue = Queue()         #Keeps ammunition drawings to refresh 
        self.__alien_squad_data = None      #The data of the alien squad
        self.__drawings_to_instance = {}    #Dictionary to convert the view
        self.__player = []                  #The player info. 1st ele (key = 0) is the Spaceship instance and the 2nd is the drawings instance.
        self.__clock = 0                    #The counter of the clock.
        self.__already_shot = False         #Tells if the player as already shot in the current clock cycle.
        self.__general_view = {}            #Contains the general skin of items.
        self.__id_to_drawings = {}          #Dictionary to convert id of canvas shapes into drawings instances.
        self.__refresh_after = None         #Keeps the last id of the self.__playground.after method.
        self.__keep_refresh = False          #Tells if we want to keep the refresh function active.
        self.__score = 0                    #Keeps the score.
        self.__is_gf_on = False             #Indicates if the frame is seeable.
        

        ##Data will be located elsewhere in a near future
        self.__alien_squad_database = [{(0, 0) : alien.Shooter, (0, 1) : alien.Alien, (0, 2) : alien.Alien, (1, 0) : alien.Alien, (1, 1) : alien.Alien, (1, 2) : alien.Shooter, 
                                        (1, 3) : alien.Shooter, (1, 4) : alien.Shooter, (1, 5) : alien.Shooter, (1, 6) : alien.Shooter, (1, 7) : alien.Shooter,
                                        (1, 8) : alien.Shooter, (1, 9) : alien.Shooter, (1, 10) : alien.Shooter, (1, 11) : alien.Shooter, (1, 12) : alien.Shooter,
                                        (2, 0) : alien.Shooter, (2, 1) : alien.Alien, (2, 2) : alien.Alien, (2, 3) : alien.Alien, (2, 4) : alien.Alien, (2, 5) : alien.Shooter, 
                                        (3, 3) : alien.Shooter, (3, 4) : alien.Shooter, (4, 5) : alien.Alien, (4, 6) : alien.Shooter, (4, 7) : alien.Shooter,
                                        (3, 8) : alien.Shooter, (4, 9) : alien.Alien, (4, 10) : alien.Shooter, (4, 11) : alien.Alien, (4, 12) : alien.Alien}]
        #self.__alien_squad_database = [{(0, 1) : 0, (0, 2) : 0, (1, 1) : 0, (0, 3) : 0,(1, 2): 0}]

        ##Tkinter
        self.__mw = Tk()
        self.__mw.title('Space Invader')
        self.__mw['bg'] = 'black'

        self.__mw_Width = self.__mw.winfo_screenwidth()             #Collects the dimension of the screen
        self.__mw_Height = self.__mw.winfo_screenheight()

        self.__Dx = (self.__mw_Width - 100) / self.__Alien_w       #Calculates the infinitesimal length
        self.__Dy = (self.__mw_Height - 200) / self.__Alien_h

        self.__mw.geometry(str(self.__mw_Width) + 'x' + str(self.__mw_Height))        

        ##Creation of frames or var initialisation
        self.__main_button_frame = Frame(self.__mw, bg = 'black')
        self.__main_button_frame.pack(side = 'bottom')

        self.__main_menu_frame = None
        self.__gaming_frame = None
        
        ##Main_button_frame building
        self.__btn_quit = Button(self.__main_button_frame, text = 'Quit', fg = 'black', command = self.__mw.destroy, font = ('Arial', int(self.__Dy * 15)))
        self.__btn_quit.pack(side = 'right', padx = 5, pady = 5)

        self.__btn_info = Button(self.__main_button_frame, text = 'à propos', fg = 'black', command = self.game_info, font = ('Arial', int(self.__Dy * 15)))
        self.__btn_info.pack(side = 'right')

        self.__btn_pause = Button(self.__main_button_frame, text = 'good bye', command = self.cancel, font = ('Arial', int(self.__Dy * 15)))   #to remove
        self.__btn_pause.pack(side = 'right')

        ##var init for main_menu_frame
        self.__game_name = None
        self.__text_last_score = None
        self.__label_last_score = None
        self.__btn_start = None

        ##var init for gaming_frame
        self.__playground = None
        # Text for life 
        self.__text_life = None
        self.__label_life = None

        # Text for Score 
        self.__text_score = None
        self.__label_score = None

        ##Bindings
        self.__key_pressed  = {"Left" : False, "Right" : False, "space" : False}      #dictionary tells (by having value = True) which key is pressed

        ##Bindings (fixed)
        for key in self.__key_pressed.keys():
            self.__mw.bind('<KeyPress-%s>' %key, self.press)
            self.__mw.bind('<KeyRelease-%s>' %key, self.release)
            
        ##Main_menu init
        self.build_main_menu()

        self.__mw.mainloop()

    def get(self):
        return self.__alien_squad_data

    def show(self, queue):
        listing = []
        for _ in range(queue.qsize()):
            item = queue.get()
            listing.append(self.__drawings_to_instance[item])
            queue.put(item)
        return listing

    def cancel(self):
        if self.__refresh_after is not None:
            self.__playground.after_cancel(self.__refresh_after)
            self.__refresh_after = None

    def spawn_alien_ammo(self, class_object, is_alien,  x_pos, y_pos, queue, direction = 1):
        '''Inputs : class_object is the class that we want to use to create the object
                is_alien is a bool that indicates if the object wanted is an alien
                x_pos and y_pos are int, describe the coords of the object to create
                queue is the queue that we want to use to keep the object updated in refresh
                direction is a int, -1 or 1, and set the direction, up or down of the ammunition, by default going down (not needed for alien)
            Outputs : the object created
            The function creates the object, its drawings and "links" them in self.__drawings_to_instance'''
        
        if is_alien:
            new_object = class_object(x_pos, y_pos)
        else:
            new_object = class_object(x_pos, y_pos, direction)

        new_object_view = self.draw(new_object.standardized_type() , new_object.x(), new_object.y())

        queue.put(new_object_view)
        self.__drawings_to_instance[new_object_view] = new_object
        return new_object

    def spawn_alien_squad(self, id):
        '''Input : id which is the index of the squad to spawn.
        No outputs. The function create the alien squad as it is described in the database.'''

        data = self.__alien_squad_database[id]
        n, p = dictio_max_key(data)
        al_squad = alien_squad.Alien_squad(n + 1, p + 1)

        for y, x in data.keys():
            new_alien = self.spawn_alien_ammo(data[(y, x)], True, x, y, self.__alien_queue)
            al_squad.add(new_alien, x, y)
        
        self.__alien_squad_data = al_squad
        al_squad.optimise()
        al_squad.allows_to_shoot()

    def spawn_spaceship(self): #To rewrite if more than 1 player
        ship = spaceship.Spaceship( 'vaisseau' , 3, 450, 900)

        ship_view = self.draw('Spaceship', ship.x(), ship.y())
        
        self.__drawings_to_instance[ship_view] = ship
        self.__player.append(ship)
        self.__player.append(ship_view)

    def refresh(self):
        Dx = self.__Dx
        Dy = self.__Dy
        al_squad = self.__alien_squad_data
        ship = self.__player[0]

        al_squad.moves()

        if al_squad.mapping == [] or al_squad.n() <= 0 or al_squad.p() <= 0:
            self.spawn_alien_squad(0)

        ##Move, refesh ammunitions with their views and manage collisions
        for _ in range(self.__ammo_queue.qsize()):
            ammo_view = self.__ammo_queue.get()
            ammo = self.__drawings_to_instance[ammo_view]
            
            ammo.moves()
            self.move_drawings(ammo_view, ammo.x(), ammo.y())
            
            #Hit detection
            item_uplet = self.__playground.find_overlapping(Dx * ammo.x(), Dy * ammo.y(), 
                                Dx * (ammo.x() + ammo.width()), Dy * (ammo.y() + ammo.height()))
            if len(item_uplet) > 1:
                nbr_hit_alien = 0
                for id in item_uplet:
                    instance = self.__drawings_to_instance[self.__id_to_drawings[id]]
                    #id is the id of the shape for canvas. It is turned into the set shapes that represents the same object. Finaly the set is turned into the object.
                    instance.hits()
                    if isinstance(instance, alien.Alien):
                        nbr_hit_alien += 1
                self.__score += nbr_hit_alien ** 2
                self.__text_score.set('Score : '+ str(self.__score))

            #Keeps only ammunition still active, others are deleted
            if ammo.is_blown_up():
                self.delete_drawings(ammo_view)
                del self.__drawings_to_instance[ammo_view]
            else:
                self.__ammo_queue.put(ammo_view)


        ##Refresh the aliens with their views
        for _ in range(self.__alien_queue.qsize()):
            alien_view = self.__alien_queue.get()
            alien_instance = self.__drawings_to_instance[alien_view]
            
            #Keeps only aliens still alive, others are deleted
            if alien_instance.is_alive():
                self.move_drawings(alien_view, alien_instance.x(), alien_instance.y())

                if alien_instance.is_allowed_shoot() and alien_instance.shoots():
                    self.spawn_alien_ammo(ammunition.Ammunition, False,  alien_instance.x() + alien_instance.width() // 2, 
                                          alien_instance.y() + alien_instance.height(), self.__ammo_queue, 1)
                self.__alien_queue.put(alien_view)

                if alien_instance.y() >= self.__player[0].y():
                    self.game_over()

            else:
                self.delete_drawings(alien_view)
                al_squad.dies(alien_instance)
                del self.__drawings_to_instance[alien_view]


        ##Refresh the spaceship, mouvment, shoots and life
        #Keyboard actions
        if self.__key_pressed['space']:
            if not(self.__already_shot):
                self.__already_shot = True
                self.spawn_alien_ammo(ammunition.Ammunition, False, ship.x() + ship.width() // 2, ship.y() - self.__Ammo_height, self.__ammo_queue, -1)

        if self.__key_pressed["Right"]:
            self.move_spaceship(True)

        if self.__key_pressed["Left"]:
            self.move_spaceship(False)
        
        #Lifes display
        self.__text_life.set('Life : '+ str(self.__player[0].life()))
        if not(self.__player[0].is_alive()):
            self.game_over()

        
        #Clock management in order not to shoot to quickly
        if self.__already_shot:
            self.__clock += 1
            if self.__clock > 20:
                self.__clock = 0
                self.__already_shot = False
        
        if self.__is_gf_on:
            Dx_tmp = self.__playground.winfo_width() / self.__Alien_w
            Dy_temp = self.__playground.winfo_height() / self.__Alien_h

            if abs(Dx_tmp - self.__Dx) > 0.001 or abs(Dy_temp - self.__Dy) > 0.001:
                self.__Dx = Dx_tmp
                self.__Dy = Dy_temp
                if self.__refresh_after is not None:
                    self.__keep_refresh = False
                    self.__refresh_after = self.__playground.after(1, self.reload_all_drawings)

        if self.__keep_refresh:
            self.__refresh_after = self.__playground.after(10, self.refresh)

    def load_views(self):
        '''to edit in order to work with the class'''
        self.__general_view['Alien'] = view.View(50, 20, [[simple_shape.Simple_shape(50, 20, 'r', 'green', '')]], 0)
        self.__general_view['Shooter'] = view.View(50, 20, [[simple_shape.Simple_shape(50, 20, 'r', 'orange', '')]], 0)
        self.__general_view['Ammunition'] = view.View(10, 20, [[simple_shape.Simple_shape(10, 20, 'r', 'white', 'red')]], 0)
        self.__general_view['Spaceship'] = view.View(10, 20, [[simple_shape.Simple_shape(100, 50, 'r', 'blue', '')]], 0)
        self.__general_view['rocks'] = view.View(10, 20, [[simple_shape.Simple_shape(20, 20, 'r', 'grey', '')]], 0)

    def build_gaming_frame(self):
        '''No inputs nor outputs. Builds gaming_frame'''
        self.__gaming_frame = Frame(self.__mw, bg = 'black')

        self.__playground = Canvas(self.__gaming_frame, width = self.__mw_Width, height = self.__mw_Height, bg = 'black')

        self.__playground.bind('<Key>', lambda x : print(x.keysym))

        # Text for life 
        self.__text_life = StringVar()
        self.__label_life = Label(self.__gaming_frame, textvariable = self.__text_life, fg = 'red', font = ('Arial', int(self.__Dy * 15)))
        self.__label_life.pack(padx = 5, pady = 5)

        # Text for Score 
        self.__text_score = StringVar()
        self.__label_score = Label(self.__gaming_frame, textvariable = self.__text_score, font = ('Arial', int(self.__Dy * 15)))
        self.__label_score.pack(padx = 5, pady = 5)

        self.__playground.pack()
        self.__gaming_frame.pack(side = 'top')

    def build_main_menu(self):
        '''No inputs nor outputs. Builds main_menu_frame'''
        self.__main_menu_frame = Frame(self.__mw, width = self.__mw_Width, height = self.__mw_Height, bg = 'black')

        self.__game_name = Label(self.__main_menu_frame, text  = 'Space Invader', bg = 'black', fg = 'red', font = ('Arial', int(self.__Dy * 70)))
        self.__game_name.pack(pady = self.__Dy * 200)

        self.__text_last_score = StringVar()
        self.__label_last_score = Label(self.__main_menu_frame, textvariable = self.__text_last_score, bg = 'black', fg = 'orange', font = ('Arial', int(self.__Dy * 15)))
        self.__label_last_score.pack(pady = self.__Dy * 2)
        
        self.__btn_start = Button(self.__main_menu_frame, text = 'Start a new game', fg = 'black', command = self.start_game, font = ('Arial', int(self.__Dy * 15)))
        self.__btn_start.pack(pady = self.__Dy * 2)

        self.__main_menu_frame.pack(side  = 'top')

    def start_game(self):
        '''No inputs nor outputs. Adjusts value of var, switching of scene and starts the game'''

        if not(self.__is_game_on):
            self.build_gaming_frame()
            self.__is_game_on = True
            self.__keep_refresh = True
            self.__score = 0
            self.__main_menu_frame.destroy()
            self.__is_gf_on = True
            self.load_views()
            self.spawn_alien_squad(self.__game_id)
            self.spawn_spaceship()
            self.refresh()
            #self.spwan_rock()  #not ready for spawning rocks

            self.__text_life.set('Life : ' + str(self.__player[0].life()))
            print('start')
            
            self.__text_score.set('Score : '+ str(self.__score))
        
    def game_over(self):
        '''No inputs nor outputs. Adjusts and resets value of var and switching of scene'''
        self.__gaming_frame.destroy()
        self.build_main_menu()

        ##Resets
        self.__is_game_on = False
        self.__keep_refresh = False
        self.__is_gf_on = False
        self.__general_view = {}
        self.__drawings_to_instance = {}
        self.__alien_squad_data = None
        self.__ammo_queue = Queue()
        self.__alien_queue = Queue()
        self.__player = []
        self.__refresh_after = None
        self.__clock = 0
        self.__already_shot = False

        ##Showing a summary
        self.__text_last_score.set('Last score : '+ str(self.__score))
        self.__main_menu_frame.pack()

    def game_info(self):
        messagebox.showinfo('à propos','Binvenue sur notre space inavader!\nCe jeu ... ')


    def draw(self, class_to_draw, x_0, y_0):
        '''Inputs : view_instance must be a instance of the class view that describes how to draw.
                    x_0 and y_0 are the position of the top left corner of the drawing.
            No outputs. The function draw the shape wanted and begins at the (x, y) coords on the canvas.'''
        
        Dx, Dy = self.__Dx, self.__Dy
        x, y = x_0, y_0
        view_to_draw = self.__general_view[class_to_draw]
        structure = view_to_draw.structure()
        compo_tmp = []

        for line_index in range(len(structure)):
            x = x_0

            for s_shape in structure[line_index]:
                x += s_shape.margin_left()

                if s_shape.shape() == 'r':
                    id = self.__playground.create_rectangle(Dx * x, Dy * y, Dx * (x + s_shape.width()), Dy * (y + s_shape.height()), 
                                        outline = s_shape.border_color(), fill = s_shape.color())
                
                elif s_shape.shape() == 'o':
                    id = self.__playground.create_oval(Dx * x, Dy * y, Dx * (x + s_shape.width()), Dy * (y + s_shape.height()), 
                                        outline = s_shape.border_color(), fill = s_shape.color())
                
                elif s_shape.shape() == 'i':
                    id = self.__playground.create_image(Dx * x, Dy * y, Dx * (x + s_shape.width()), Dy * (y + s_shape.height()))
                
                compo_tmp.append(id)
                x += s_shape.margin_right()
            
            y += view_to_draw.interline(line_index)

        drawings = drawing.drawing(x_0, y_0, compo_tmp)

        for id in compo_tmp:
            self.__id_to_drawings[id] = drawings

        return drawings

    def move_drawings(self, drawings, x, y):
        Dx, Dy = self.__Dx, self.__Dy
        delta_x = x - drawings.x()      #variation between de old position of the hole drawing and the new one
        delta_y = y - drawings.y()      #/!\ At the absolute scale (object-oriented scale)
        
        for s_shape_id in drawings.drawings():
            i, j, k , l = self.__playground.coords(s_shape_id)         #Get the old position of the shape, not the hole drawing. /!\ At the scale of the canvas (may differ of the object-oriented scale) 
            self.__playground.coords(s_shape_id, i + Dx * delta_x, j + Dy * delta_y, k + Dx * delta_x, l + Dy *delta_y)

        drawings.set_coords(x, y)

    def delete_drawings(self, drawings):
        for s_shape_id in drawings.drawings():
            self.__playground.delete(s_shape_id)

    def reload_all_drawings(self):

        old_view_to_instance = self.__drawings_to_instance
        self.__drawings_to_instance = {}
        self.__alien_queue = Queue()
        self.__ammo_queue = Queue()

        for view_to_reload in old_view_to_instance:
            self.delete_drawings(view_to_reload)
            instance_to_reload = old_view_to_instance[view_to_reload]
            std_type = instance_to_reload.standardized_type()
            drawings = self.draw(std_type, instance_to_reload.x(), instance_to_reload.y())
            self.__drawings_to_instance[drawings] = instance_to_reload

            if std_type == 'Ammunition':
                self.__ammo_queue.put(drawings)

            elif std_type in ['Alien', 'Shooter']:
                self.__alien_queue.put(drawings)

            else:
                self.__player[1] = drawings
        
        self.__keep_refresh = True
        self.__refresh_after = self.__playground.after(9, self.refresh)

    ################################################   spwan rock   #################################################### Not finished

    # def spwan_little_rock(self, width_rock, height_rock):
    #     little_rock  = self.__playground.create_rectangle(width_rock - 10, height_rock - 200, width_rock + 10, height_rock - 180, outline = 'black', fill = 'grey')

    # def spwan_rock(self):
    #     width_rock = 50
    #     rock_list = [rock.Rock(), rock.Big(), rock.Donut(), rock.Triangle()]
    #     for number_rock in range (3):
    #         #choose 1 type of rock
    #         rock_choose = rock_list[randint(0, len(rock_list)) - 1]
    #         print (rock_choose)
    #         for colum in range(rock_choose.number_rock_colum()):
    #             height_rock = self.__mw_Height - 200
    #             width_rock  += 20

    #             for line in range(rock_choose.number_rock_line()) :

    #                 if rock_choose.create_rock(line, colum):
    #                     self.spawn_alien_ammo(self, class_object, False,  x_pos, y_pos, queue, direction = 1)

    #                 height_rock += 20

    #         width_rock  += 100




    ############################################################### Move the spaceship #####################################################################

    def move_spaceship(self, direction):
        ship = self.__player[0]
        ship.move(direction) #100 = line of the spaceship
        self.move_drawings(self.__player[1], ship.x(), ship.y())
            

    #turn True in key_press, the bind you press in game
    def press(self, event):
        self.__key_pressed[event.keysym] = True

    #turn False in key_press, the bind you release in game
    def release(self, event):
        self.__key_pressed[event.keysym] = False

    #######################################################################################################################################################


if __name__ == "__main__":
    cache.append(Space_invader())