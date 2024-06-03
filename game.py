from random import choice
from turtle import onclick
import pygame
from player import player
from tile_system import game_tiles
import pygame_menu
import csv
import urllib3
import time

class game:
    def __init__(self, tile_size: int, player_size: list[int], player_speed: float, animation_rate: int, start_index: list[int]):
        
        self.menu_theme = pygame_menu.themes.THEME_GREEN
        self.menu_theme.border_width = 0
        self.menu_theme.title_background_color = (20, 60, 10)
        self.menu_theme.background_color = (50, 110, 10)
        self.font_size = 300
        self.menu_theme.widget_font_shadow = True
        self.menu_theme.widget_font_shadow_color = (100, 100, 255)
        self.menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
        self.menu_theme.widget_font = './assets/fonts/ThaleahFat.ttf'
        self.menu_theme.title_font = './assets/fonts/ThaleahFat.ttf'
        self.menu_theme.title_font_size = 80
        self.menu_theme.selection_color = (200, 200, 255)
        
        self.bg_music = pygame.mixer.Sound('./assets/sounds/bg_music.mp3')
        self.ui_music = pygame.mixer.Sound('./assets/sounds/menu_switch.mp3')
        self.game_over_music = pygame.mixer.Sound('./assets/sounds/game_over.mp3')
        self.win_music = pygame.mixer.Sound('./assets/sounds/you_won.mp3')
        self.sound_channel = pygame.mixer.Channel(0)
        self.ui_sound_channel = pygame.mixer.Channel(1)

        self.tiles = game_tiles(tile_size, player_speed)
        self.player = player(player_size, animation_rate, self.tiles.index_to_coord(start_index))
        self.start_index = start_index
        self.animation_rate = animation_rate
        self.player_size = player_size
        self.inputs = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
        self.player_index = start_index
        self.t1 = pygame.time.get_ticks()
        self.t2 = pygame.time.get_ticks()
        self.player_destination = self.player.rect.center
        
        self.speed = [0, 0]
        self.current_context = self.handle_home_menu
        self.current_draw = self.render_home_menu
        
        # Create the game menus
        # the home menu       
        self.info_menu = pygame_menu.Menu("Instructions", 700, 600, theme=self.menu_theme)
        self.info_menu.add.label("Make your way to the treasure box")
        self.info_menu.add.label("Points: ")
        self.info_menu.add.label("Blue Diamond = 50 points")
        self.info_menu.add.label("Gold = 15 points")
        self.info_menu.add.label("Silver = 10 points")
        self.info_menu.add.label("Red = 5 points")
        self.info_menu.add.label("Black = 1 point")

        self.info_menu.add.label("Controls:")
        self.info_menu.add.label("W         Up")
        self.info_menu.add.label("A         Down")
        self.info_menu.add.label("S         Left")
        self.info_menu.add.label("D         Right")
        
        self.info_menu.add.label("Finish with 20 seconds to earn extra points")
        self.info_menu.add.button("Start", self.select_username)
        self.info_menu.add.button("Back", self.show_home_menu)
    
        self.home_menu = pygame_menu.Menu("ECO PLAY", 600, 400, theme=self.menu_theme)
        self.home_menu.add.button("Play", self.show_objective_menu, font_size=60)
        self.home_menu.add.button("Top scores", self.select_top_scores, font_size=60)
        self.home_menu.add.button("Settings", self.select_settings, font_size=60)
        self.home_menu.add.button("Exit game", self.kill_game, font_size=60)
        
        self.game_over = pygame_menu.Menu("You won", 600, 400, theme=self.menu_theme)
        self.game_over.add.label(f"Score {0}")
        self.game_over.add.button("Return to Main Menu", self.show_home_menu)
        self.game_over.add.button("Exit game", self.kill_game)
        
        self.settings_menu = pygame_menu.Menu("Settings", 600, 400, theme=self.menu_theme)
        self.settings_menu.add.range_slider("Volume", 1, (0, 1), 0.1, self.sound_channel.set_volume)
        self.settings_menu.add.button("Back", self.show_home_menu)
        
        self.user_name_menu = pygame_menu.Menu("Input", 600, 400, theme=self.menu_theme)
        self.user_name_menu.add.text_input("Username: ", maxchar=12, input_underline='_', onreturn=self.show_username, font_size=50)
        
        self.results_menu = pygame_menu.Menu("Results", 600, 400, theme=self.menu_theme)
        
        self.max_time = 65*1000 # In milliseconds
        self.start_time = 0
        self.time_left = 0
        self.score = 0
        
        self.font_obj = pygame.font.Font("./assets/fonts/ThaleahFat.ttf", 45)
        
        # Create the top scores table
        self.table_id = None
        self.players_list = []
        self.player_data = self.load_best_scores()
        self.player_name = ""
        self.top_scores_table = None
        self.create_top_scores_table()
        
        # Create the pop up menu items
        self.pop_up = pygame_menu.Menu("Hint", 600, 400, theme=self.menu_theme)
        self.canvas = pygame.surface.Surface((840, 640))
        self.hint_timer1 = 0
        self.hint_timer2 = 0
        self.hint_duration = 5000               # pop up menus last for 5 seconds
        self.hint_cooldown = 12500              # Time in between pop up menus
        
        self.database = './assets/game_data/data_csv.csv'
        self.events_que = []
        self.alive = True
        self.game_clock = pygame.time.Clock()
        self.FPS = 90
        
        self.volume = 1

    def update(self):
        self.events_que = pygame.event.get()
        for event in self.events_que:
            if event.type == pygame.QUIT:
                self.kill_game()
        self.current_context()

        
    def draw(self, screen: pygame.Surface):
        self.current_draw(screen)
        
    def kill_game(self):
        self.alive = False
        
    def run(self, screen: pygame.Surface):
        self.sound_channel.play(self.bg_music, -1)
        while self.alive:
            screen.fill((20, 60, 10))
            self.update()
            self.draw(screen)        
            pygame.display.flip()
            self.game_clock.tick(self.FPS)
        self.sound_channel.pause()
    """===============================================================================================
        These methods hand over control from one game item to another, eg home menu to settings menu
    ================================================================================================="""
    def select_settings(self):
        self.ui_sound_channel.play(self.ui_music)
        self.current_context = self.handle_settings
        self.current_draw = self.render_settings_menu
        

    def select_username(self):
        self.ui_sound_channel.play(self.ui_music)
        self.current_context = self.handle_user_input
        self.current_draw = self.render_user_input
        
    def select_top_scores(self):
        self.ui_sound_channel.play(self.ui_music)
        self.current_context = self.handle_top_scores
        self.current_draw = self.render_top_scores
        
    def show_game_over_menu(self):
        self.ui_sound_channel.play(self.ui_music)
        if self.player_data[self.player_name] < self.score:
            self.player_data[self.player_name] = self.score
            # Add the players score to the top scores table
            self.table_id.add_row((f"    {self.player_name}    ", f"    {self.score}    "), cell_align=pygame_menu.locals.ALIGN_CENTER)
        self.current_context = self.handle_game_over_menu
        self.current_draw = self.render_game_over_menu  
        
    def show_objective_menu(self):
        self.ui_sound_channel.play(self.ui_music)
        self.current_context = self.handle_info_menu
        self.current_draw = self.render_info_menu
        
    def start_game(self):
        self.ui_sound_channel.play(self.ui_music)
        self.start_time = pygame.time.get_ticks()
        self.current_context = self.update1
        self.current_draw = self.game_draw
        
    def show_home_menu(self):
        self.ui_sound_channel.play(self.ui_music)
        self.current_context = self.handle_home_menu
        self.current_draw = self.render_home_menu  
        
    def show_username(self, username: str):
        self.ui_sound_channel.play(self.ui_music)
        self.player_name = username
        if username not in self.players_list:
            self.players_list.append(username)
            self.player_data[username] = 0
        self.start_game()
        self.hint_timer1 = pygame.time.get_ticks()
        self.hint_timer2 = pygame.time.get_ticks()
    """=============================================================================================
        These methods are used to communicate with the game's database
            They load LA and LB, 
            Keep track of the top scores using a locally stored text file
            Fecth data at the end of the game from the csv file
    ================================================================================================"""
    
    def find_score_in_database(self, score: str):
        reading_column_index = 6
        with open(self.database, 'r', encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)                   # Does not need to load the whole file into memory
            for row in reader:
                if row[reading_column_index] == score:      # Look for the column with the same score as the given score
                    return row
                

    def load_energy_tipsA(self):
        energy_list_A = [];
        with open("./assets/game_data/ListA.txt") as tips:
            line = "start"
            while line != "":
                try:
                    line = tips.readline()
                    if line != "":
                        energy_list_A.append(line)
                except IOError:
                    print("Error: Cannot read file.")
                    return None
        return energy_list_A
    
    
    def load_energy_tips_B(self):
        energy_list_B = []
        with open("./assets/game_data/ListB.txt") as tips:
            line = "start"
            while line != "":
                try:
                    line = tips.readline()
                    if line != "" and line != '\n':
                        energy_list_B.append(line)
                except IOError:
                    print("Error: Cannot read file.")
                    return None
        return energy_list_B
    

    def load_best_scores(self):
        scores = {}
        with open("./assets/game_data/best_scores.txt") as best_scores:
            line = "start"
            while line != "":
                try:
                    line = best_scores.readline()
                    if line != "":
                        info = line.split(',')
                        scores[info[0]] = int(info[1])
                except IOError:
                    print("Error: Cannot read file.")
                    return None
        return scores
    

    """===============================================================
        Render methods, these render various game components such as 
        menus and the game itself.
    =================================================================="""
    
    def render_results_menu(self, screen: pygame.Surface):
        self.results_menu.draw(screen)
        
    def render_pop_up(self, screen: pygame.Surface):
        screen.blit(self.canvas, (0, 0))
        
    def render_user_input(self, screen: pygame.Surface):
        self.user_name_menu.draw(screen)
        
    def render_home_menu(self, screen: pygame.Surface):
        self.home_menu.draw(screen)
 
    def render_info_menu(self, screen: pygame.Surface):
        self.info_menu.draw(screen)
        
    def render_game_over_menu(self, screen: pygame.Surface):
        self.game_over.draw(screen)
        
    def render_top_scores(self, screen: pygame.Surface):
        self.top_scores_table.draw(screen)
        
    def render_settings_menu(self, screen: pygame.Surface):
        self.settings_menu.draw(screen)
        
    """=============================================================
        Event handlers, update various game components on what the
        player is doing, eg clicking their mouse, etc
    ================================================================"""
            
    def handle_pop_up(self):
        self.hint_timer2 = pygame.time.get_ticks()
        if self.hint_timer2 - self.hint_timer1 > self.hint_duration:
            self.current_context = self.update1
            self.current_draw = self.game_draw
            self.hint_timer1 = pygame.time.get_ticks()
            self.hint_timer2 = pygame.time.get_ticks()
            self.start_time += self.hint_duration
            
    def handle_top_scores(self):
        self.top_scores_table.update(self.events_que)
        
    def handle_settings(self):
        self.settings_menu.update(self.events_que)
        
    def handle_user_input(self):
        self.user_name_menu.update(self.events_que)
                    
    def handle_results_menu(self):
        self.results_menu.update(self.events_que) 
        
    def handle_home_menu(self):
        self.home_menu.update(self.events_que)
        
    def handle_info_menu(self):
        self.info_menu.update(self.events_que)
        
    def handle_game_over_menu(self):
        self.game_over.update(self.events_que)
        
    def update1(self):
        self.time_left = self.max_time - (pygame.time.get_ticks() - self.start_time)
        self.event_handler()
        self.player.update()
        pygame.sprite.spritecollide(self.player, self.tiles.coins1, True)
        pygame.sprite.spritecollide(self.player, self.tiles.coins2, True)
        pygame.sprite.spritecollide(self.player, self.tiles.coins3, True)
        pygame.sprite.spritecollide(self.player, self.tiles.coins4, True)
        pygame.sprite.spritecollide(self.player, self.tiles.coins5, True)
        
        self.hint_timer2 = pygame.time.get_ticks()
        if self.hint_timer2 - self.hint_timer1 > self.hint_cooldown and self.time_left > 4:
            self.hint_timer1 = pygame.time.get_ticks()
            self.create_pop_up()
            self.current_context = self.handle_pop_up
            self.current_draw = self.render_pop_up
        
    def event_handler(self):
        pygame.event.get()
        keys = pygame.key.get_pressed()
        self.t2 = pygame.time.get_ticks()     

        if self.player.rect.centerx != self.player_destination[0] or self.player.rect.centery != self.player_destination[1]:
            self.player.rect.centerx += self.speed[1]
            self.player.rect.centery += self.speed[0]
            self.player.update_animation_position(self.player.rect.center)
            return
        else:
            self.sound_channel.pause()
            self.speed = [0, 0]
            if self.tiles.has_won(self.player_index):
                self.current_context = self.handle_results_menu
                self.current_draw = self.render_results_menu
                self.score += 10            # Bonus points for finishing the game
                self.create_results_menu(True)
                self.ui_sound_channel.play(self.win_music)
                if self.player_data[self.player_name] < self.score:
                    self.player_data[self.player_name] = self.score
                    # Update the top scores list and tables
                    self.write_top_scores_list()
                    self.player_data = self.load_best_scores()
                    self.create_top_scores_table()  
                # Reset the game
                self.player = player(self.player_size, self.animation_rate, self.tiles.index_to_coord(self.start_index))
                self.player_index = self.start_index
                self.player_destination = self.player.rect.center
                self.time = self.max_time
                self.tiles.load_coins()
            elif self.time_left <= 0:
                self.current_context = self.handle_results_menu
                self.current_draw = self.render_results_menu
                self.create_results_menu(False)
                self.ui_sound_channel.play(self.game_over)
                # Reset the game
                self.player = player(self.player_size, self.animation_rate, self.tiles.index_to_coord(self.start_index))
                self.player_index = self.start_index
                self.player_destination = self.player.rect.center
                self.time = self.max_time
                self.tiles.load_coins()
                
            self.sound_channel.unpause()
            
                
        for input_option in self.inputs:
            if keys[input_option]:
                [new_index, new_animation, speed] = self.tiles.get_next_index(self.player_index, input_option)
                if new_index != None and speed != None and new_animation != None:
                    self.player_index = new_index
                    self.player_destination = self.tiles.index_to_coord(self.player_index)
                    self.speed = speed  
                    
    def game_draw(self, screen):
        self.tiles.draw(screen)
        self.player.draw(screen)
        self.score = round(self.time_left/1000) + self.tiles.compute_score()
        timer_banner = self.font_obj.render(f"Time left :{round(self.time_left/1000)}", True, (0, 0, 0))
        score_banner = self.font_obj.render(f"Score: {self.score}", True, (0, 0, 0))
        timer_pos = timer_banner.get_rect()
        timer_pos.left = 200
        timer_pos.top = 540
        
        score_pos = score_banner.get_rect()
        score_pos.left = 500
        score_pos.top = 540
        
        screen.blit(timer_banner, timer_pos)
        screen.blit(score_banner, score_pos)
        
    """================================================================
        These create game components which may change throughtout the
        course of the game, these include the pop up screens during the 
        game, the top scores table etc    
    ===================================================================="""
    
    def create_top_scores_table(self):
        self.top_scores_table = pygame_menu.Menu("Top scores", 600, 400, theme=self.menu_theme)
        
        scores = self.load_best_scores()
        table = self.top_scores_table.add.table(table_id="1", font_size=40)
        self.table_id = table
        table.default_call_padding = 100
        # Check for an empty table
        for key in scores.keys():
            table.add_row((f"    {key}    ", f"    {scores[key]}    "), cell_align=pygame_menu.locals.ALIGN_CENTER)
            self.players_list.append(key)
            
        self.top_scores_table.add.button("Back", self.show_home_menu)
        
    
    def create_pop_up(self):
        hints_temp = self.load_energy_tipsA()
        hints = []
        for hint in hints_temp:
            if hint != '\n':
                hints.append(hint)
        self.pop_up = pygame_menu.Menu("Energy Tip!", 800, 300, theme=self.menu_theme)
       
        hint = choice(hints)
        self.pop_up.add.label(hint, wordwrap=True)
        self.current_draw(self.canvas)
        self.pop_up.draw(self.canvas)
      
        
    def create_results_menu(self, has_won: bool):
        message = "You won!" if has_won else "Sorry, you lost."
        self.results_menu = pygame_menu.Menu("Results", 840, 600, theme=self.menu_theme)
        self.results_menu.add.label(message)
        self.results_menu.add.label(f"Score {self.score}")
        self.results_menu.add.label(f"Current temperature {game.get_current_temperature()}")
        if has_won:
            row = self.find_score_in_database(str(self.score))
            if row:
                table = self.results_menu.add.table("info", font_size=17)
                table.add_row([" Sensor ID ", " Description ", " Unit ", " Info Province ", "Info Manucipalicty", " Date ", " Temperature "])
                
                del row[6]
                # Pad the items
                for i in range(len(row)):
                    newStr = "  " + row[i] + "  "
                    row[i] = newStr
                table.add_row(row)
                list_b = self.load_energy_tips_B()
                choosen_hint = choice(list_b)
                self.results_menu.add.label("Heres some information")
                self.results_menu.add.label(choosen_hint, wordwrap=True)
        else:
            list_b = self.load_energy_tips_B()
            choosen_hint = choice(list_b)
            self.results_menu.add.label("Heres some information")
            self.results_menu.add.label(choosen_hint, wordwrap=True)
        self.results_menu.add.button("Home", self.show_home_menu)
        

    def write_top_scores_list(self):
        with open("./assets/game_data/best_scores.txt", 'w') as best_scores_file:
                for player in list(self.player_data.keys()):
                    best_scores_file.write(f"{player},{self.player_data[player]}\n")

    @staticmethod
    def get_current_temperature():
        data = urllib3.request('GET', 'https://api.open-meteo.com/v1/forecast?latitude=50.75&longitude=4.5&hourly=temperature_2m')
        data = data.json()["hourly"]["temperature_2m"]
        hour = time.localtime().tm_hour
        return data[hour]