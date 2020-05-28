import sys
import pygame
from pygame.sprite import Sprite
from pygame import image as pyimage, time as pytime, font as pyfont
import random


class Settings:
    """ A class to store all settings for a game """

    def __init__(self):
        """ Initialize the game's settings """

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.play_bg_color = (169, 151, 190)
        self.bg_color = (255, 255, 255)

        self.purpy_speed = 10
        self.velocity = 2000

        # flags
        self.intro_active = True
        self.game_active = False
        self.showme_active = False
        self.message_active = False
        self.drowing_active = False

        self.spots = [
            (150, 50), (150, 100), (150, 150), (150, 200), (150, 250),
            (200, 150), (250, 150),
            (300, 50), (300, 100), (300, 150), (300, 200), (300, 250),

            (450, 50), (450, 100), (450, 150), (450, 200), (450, 250),

            (600, 50), (600, 100), (600, 150), (600, 200), (600, 250),
            (650, 50), (700, 50), (730, 100), (700, 150), (650, 150),
            (680, 200), (720, 250),

            (850, 50), (850, 100), (850, 150), (850, 200), (850, 250),
            (900, 50), (950, 50),
            (900, 150),
            (900, 250), (950, 250),

            (300, 450), (300, 500), (300, 550), (300, 600), (300, 650),
            (350, 500), (380, 550), (420, 550), (460, 500),
            (500, 450), (500, 500), (500, 550), (500, 600), (500, 650),

            (600, 450), (600, 500), (600, 550), (600, 600), (600, 650),
            (650, 450), (700, 450),
            (650, 550),
            (650, 650), (700, 650),

            (830, 500), (830, 600),

            (900, 450), (900, 500), (900, 550), (900, 600), (900, 650),
            (950, 450), (1000, 450), (1050, 500), (1050, 550), (1050, 600), (1000, 650), (950, 650)
        ]

    def set_bg_color(self):
        if self.game_active is True:
            self.bg_color = (169, 151, 190)
        else:
            self.bg_color = (255, 255, 255)
        return self.bg_color


class Purpy:
    """ A class to manage purpy """

    def __init__(self, flea_game):
        """ Initilaize purpy and set it's starting position """
        self.settings = flea_game.settings
        self.screen = flea_game.screen
        self.screen_rect = flea_game.screen.get_rect()

        # load the images and set the first one
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()


        self.rect.midbottom = self.screen_rect.midbottom
        self.y = float(self.rect.y)

        # Set flags
        self.move_down = False
        self.move_up = False
        self.drown = False
        self.drowning_exit = False
        self.blinked = False
        self.current_frame = 0
        self.last_update = 0

        self.intro_messages = [Message(self, "Hey! It's Purpy.", ),
                         Message(self, "Basically, I'm a very hygienic and clean creature - I bath every 7 minutes.", 50),
                         Message(self, "And somehow I got fleas!", 100),
                         Message(self, 'Will you help me kill them?', 150)]

    def load_images(self):
        """Load all images for purpy's behaviour """
        self.image_smile = pyimage.load('images/purpy/purpy.bmp')
        self.image_sad = pyimage.load('images/purpy/purpy_sad.bmp')
        self.image_ear = pyimage.load('images/purpy/purpy_left_ear.bmp')
        self.image_eyes1 = pyimage.load('images/purpy/purpy_close_eyes1.bmp')
        self.image_eyes2 = pyimage.load('images/purpy/purpy_close_eyes2.bmp')
        self.image_eyes3 = pyimage.load('images/purpy/purpy_close_eyes3.bmp')

        # frames for animations
        self.standing_frames = [self.image_smile, self.image_eyes1, self.image_eyes2, self.image_eyes3]
        self.ear_frames = [self.image_smile, self.image_ear, self.image_ear, self.image_smile,
                           self.image_ear, self.image_ear, self.image_smile]

    def set_image(self, image):
        """Set image for purpy"""
        self.image = image

    def _animation(self, frames, now, delay = None):
        self.current_frame = (self.current_frame + 1) % len(frames)
        self.image = frames[self.current_frame]
        if self.current_frame == 0:
            self.last_update = now

    def animate(self):
        """Animate purpy's behaviour"""
        now = pytime.get_ticks()
        self.set_image(self.image_smile)
        if now - self.last_update > 2000:
            self._animation(self.standing_frames, now)

    def update_face_drowns(self):
        if self.rect.bottom > self.screen_rect.bottom:
            self.set_image(self.image_sad)

    def drowning(self):
        self.settings.game_active = False
        self.settings.drowning_active = True
        self.settings.drowing_active = True
        if self.rect.top > self.screen_rect.bottom:
            self.drown = True

    def update_position(self, speed):
        """ Update purpy's position based on moving flag """
        if self.move_up and self.rect.bottom > self.screen_rect.bottom:
            self.rect.y -= speed
            self.settings.drowing_active = False
        if self.move_down:
            self.rect.y += speed / 2
            self.drowning()

    def update(self):
        self.animate()
        self.update_position(self.settings.purpy_speed)
        self.update_face_drowns()

    def blitme(self):
        """ Draw the ship in it's current location """
        self.screen.blit(self.image, self.rect)


class Flea(Sprite):

    """ A class to manage flea sprite """
    def __init__(self, flea_game, number):
        super().__init__()

        self.game = flea_game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.number = number

        self.image_alive = pygame.image.load('images/flea2.bmp')
        self.image_killed = pygame.image.load('images/flea_killed.bmp')
        self.image = self.image_alive
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

    def kill(self):
        self.image = self.image_killed
        self.draw()

    def update(self):
        self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Button:

    def __init__(self, flea_game, type):
        self.screen = flea_game.screen
        self.screen_rect = self.screen.get_rect()
        self.type = type
        self.load_images()
        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.current_frame = 0
        self.last_update = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def load_images(self):
        self.image_play = pyimage.load('images/play_button.bmp')
        self.image_showme = pyimage.load('images/showme/sm1.bmp')
        self.showme_frames = [pyimage.load('images/showme/sm1.bmp'),pyimage.load('images/showme/sm2.bmp'),
                              pyimage.load('images/showme/sm3.bmp'),pyimage.load('images/showme/sm4.bmp'),
                              pyimage.load('images/showme/sm5.bmp'), pyimage.load('images/showme/sm6.bmp'),
                              pyimage.load('images/showme/sm7.bmp'), pyimage.load('images/showme/sm8.bmp'),
                              pyimage.load('images/showme/sm9.bmp'), pyimage.load('images/showme/sm10.bmp'),
                              pyimage.load('images/showme/sm11.bmp'), pyimage.load('images/showme/sm12.bmp'),
                              pyimage.load('images/showme/sm13.bmp'), pyimage.load('images/showme/sm14.bmp'),
                              pyimage.load('images/showme/sm15.bmp'), pyimage.load('images/showme/sm16.bmp'),
                              pyimage.load('images/showme/sm17.bmp'), pyimage.load('images/showme/sm18.bmp'),
                              pyimage.load('images/showme/sm19.bmp'), pyimage.load('images/showme/sm20.bmp'),
                              pyimage.load('images/showme/sm21.bmp'), pyimage.load('images/showme/sm22.bmp'),
                              pyimage.load('images/showme/sm23.bmp'), pyimage.load('images/showme/sm24.bmp'),
                              pyimage.load('images/showme/sm25.bmp'), pyimage.load('images/showme/sm26.bmp'),
                              pyimage.load('images/showme/sm27.bmp'), pyimage.load('images/showme/sm28.bmp'),
                              pyimage.load('images/showme/sm29.bmp'), pyimage.load('images/showme/sm30.bmp'),
                              pyimage.load('images/showme/sm31.bmp'), pyimage.load('images/showme/sm32.bmp'),
                              pyimage.load('images/showme/sm33.bmp'), pyimage.load('images/showme/sm34.bmp'),
                              pyimage.load('images/showme/sm35.bmp'), pyimage.load('images/showme/sm36.bmp'),
                              pyimage.load('images/showme/sm37.bmp'), pyimage.load('images/showme/sm38.bmp'),
                              pyimage.load('images/showme/sm38.bmp'), pyimage.load('images/showme/sm38.bmp'),
                              pyimage.load('images/showme/sm38.bmp'), pyimage.load('images/showme/sm38.bmp'),
                              pyimage.load('images/showme/sm38.bmp'), pyimage.load('images/showme/sm38.bmp'),
                              pyimage.load('images/showme/sm38.bmp'), pyimage.load('images/showme/sm38.bmp'),
                              pyimage.load('images/showme/sm27.bmp'),
                              pyimage.load('images/showme/sm26.bmp'), pyimage.load('images/showme/sm25.bmp'),
                              pyimage.load('images/showme/sm24.bmp'), pyimage.load('images/showme/sm23.bmp'),
                              pyimage.load('images/showme/sm22.bmp'), pyimage.load('images/showme/sm21.bmp'),
                              pyimage.load('images/showme/sm20.bmp'), pyimage.load('images/showme/sm19.bmp'),
                              pyimage.load('images/showme/sm18.bmp'), pyimage.load('images/showme/sm17.bmp'),
                              pyimage.load('images/showme/sm16.bmp'), pyimage.load('images/showme/sm15.bmp'),
                              pyimage.load('images/showme/sm14.bmp'), pyimage.load('images/showme/sm13.bmp'),
                              pyimage.load('images/showme/sm12.bmp'), pyimage.load('images/showme/sm11.bmp'),
                              pyimage.load('images/showme/sm10.bmp'), pyimage.load('images/showme/sm9.bmp'),
                              pyimage.load('images/showme/sm8.bmp'), pyimage.load('images/showme/sm8.bmp'),
                              pyimage.load('images/showme/sm6.bmp'), pyimage.load('images/showme/sm5.bmp'),
                              pyimage.load('images/showme/sm4.bmp'), pyimage.load('images/showme/sm3.bmp'),
                              pyimage.load('images/showme/sm2.bmp'), pyimage.load('images/showme/sm1.bmp'),
                              ]

    def set_image(self):
        if self.type == 'play':
            self.image = self.image_play
        elif self.type == 'showme':
            self.image = self.image_showme

    def _animation(self, frames, now, delay = None):
        self.current_frame = (self.current_frame + 1) % len(frames)
        self.image = frames[self.current_frame]
        if delay:
            if self.current_frame == delay:
                pytime.delay(100)
        if self.current_frame == 0:
            self.last_update = now

    def animate(self):
        now = pytime.get_ticks()
        if now - self.last_update > 300:
            self._animation(self.showme_frames, now)

    def update(self):
        self.animate()


class Message:

    def __init__(self, game, msg=None, below=0, right=0, left=0, background = (255, 255, 255), transparent = False):
        """Initialize message attributes"""
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.font = pyfont.SysFont(None, 38)
        self.below = below
        self.right = right
        self.left = left
        self.msg = msg
        self.background = background
        self.transparent = transparent

        # prep message
        self.prep(msg)

    def set_text(self, text):
        self.msg = text

    def put_below(self):
        if self.below > 0:
            self.msg_rect.y += self.below

    def move_from_center(self):
        if self.right > 0:
            self.msg_rect.x += self.right
        if self.left > 0:
            self.msg_rect.x -= self.left

    def prep(self, msg):
        """ Render message into an image and place it center it """
        self.msg_image = self.font.render(msg, True, (0,0,0), self.background)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.centerx = self.screen_rect.centerx
        self.msg_rect.y = 70
        self.put_below()
        self.move_from_center()
        self.set_transparent(self.msg_image)

    def set_transparent(self, image):
        if self.transparent is True:
            image.set_alpha(100)

    def blit(self):
        self.screen.blit(self.msg_image, self.msg_rect)


class PurpyFleas:
    """ Overall class to manage game assets and behaviour """

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Purpy has fleas!')
        self.screen.fill(self.settings.set_bg_color())

        self.purpy = Purpy(self)
        self.fleas = pygame.sprite.Group()
        self.play_button = Button(self, 'play')
        self.showme_button = Button(self, 'showme')


        self.available_fleas = []
        self.last_flea_drawn = 0
        self.last_message = 0
        self.last_killed = 0
        self.message_flea = 0
        self.last_refill = 0

        self.killed_fleas = []
        self.current_flea = []
        self.drawn_fleas = []
        self._create_fleas()

    def _check_play_button(self, mouse_pos):
        """ Check if mouse clicked on button and start a game if so"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.settings.intro_active, self.settings.game_active = False, True

    def _create_flea(self, number):
        """ Create a single flea in available spot """
        flea = Flea(self, number)
        spot = self.settings.spots[random.randint(0, len(self.settings.spots)-1)]
        flea.rect.x, flea.rect.y = spot
        self.settings.spots.remove(spot)
        self.fleas.add(flea)

    def _create_fleas(self):
        last_flea = 0
        for i in range(len(self.settings.spots)):
            self._create_flea(last_flea)
            last_flea += 1
        self.available_fleas = [x for x in range(len(self.fleas.sprites()))]

    def _check_if_alive(self, chosen_flea):
        if chosen_flea in self.killed_fleas: return False
        return True

    def _get_flea(self, flea_number):
        for flea in self.fleas:
            if flea.number == flea_number:
                return flea

    def _show_fleas(self):
        if len(self.available_fleas) > 0:
            now = pygame.time.get_ticks()
            chosen_flea = random.choice(self.available_fleas)
            flea = self._get_flea(chosen_flea)
            if now - self.last_flea_drawn > self.settings.velocity:
                flea.draw()
                self.last_flea_drawn = now
                self.drawn_fleas.append(chosen_flea)
                self.current_flea.append(flea)

    def _check_events(self):
        """ Respond to keyboard and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.settings.intro_active is True:
                    self._check_play_button(mouse_pos)
                elif self.settings.showme_active is True:
                    self._check_showme_button(mouse_pos)
                else:
                    self._check_flea_killed(mouse_pos)
            elif event.type == pygame.KEYUP:
                self.purpy.move_down, self.purpy.move_up = False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.purpy.move_down = True
                if event.key == pygame.K_UP:
                    self.purpy.move_up = True

    def _check_flea_killed(self, mouse_pos):
        for flea in self.current_flea:
            if flea.rect.collidepoint(mouse_pos):
                flea.kill()
                self.update_level()
                if flea.number not in self.killed_fleas: self.killed_fleas.append(flea.number)
                try:
                    self.available_fleas.remove(flea.number)
                except ValueError:  # double click on a flea
                    pass

    def _check_status(self):
        if self.settings.game_active is True and self.settings.message_active is False:
            if len(self.killed_fleas) == len(self.fleas.sprites()):
                self.settings.game_active, self.settings.showme_active = False, True
                self.screen.fill(self.settings.play_bg_color)

    def update_level(self):
        if len(self.killed_fleas) % int((len(self.fleas)*0.1)) == 0 and len(self.killed_fleas) > 0:
            self.settings.velocity -= 100

    def _check_showme_button(self, mouse_pos):
        if self.showme_button.rect.collidepoint(mouse_pos):
            self.settings.showme_active, self.settings.message_active = False, True
            self.screen.fill(self.settings.play_bg_color)

    def _show_final_message(self):
        self.available_fleas.clear()
        now = pygame.time.get_ticks()
        if now - self.last_message > 300:
            try:
                self._get_flea(self.killed_fleas[self.message_flea]).draw()
                self.message_flea += 1
                self.last_message = now
            except IndexError:  # end of list
                pass

    def _show_intro_message(self):
        if self.settings.intro_active is True and self.settings.drowing_active is False:
            for msg in self.purpy.intro_messages:
                msg.blit()
            self.play_button.draw()

    def _show_bye_message(self):
        if self.settings.drowing_active is True:
            Message(self, 'ok. bye.', below=200).blit()

    def _show_score(self):
        Message(self, f"{str(len(self.killed_fleas))}/{str(len(self.fleas))}", right=500,
                background=self.settings.play_bg_color).blit()

    def _quit_when_drown(self):
        """ Quit game when purpy goes down lower than the screen """
        if self.purpy.drown is True and self.settings.intro_active is True:
            sys.exit()

    def _update_screen(self):
        """ Update images to the screen and flip to the new screen """
        if self.settings.intro_active is True:
            self.purpy.blitme()
            self._show_intro_message()
            self._show_bye_message()
        elif self.settings.game_active is True:
            self.settings.intro_active = False
            self._check_status()
            self._show_fleas()
            self._show_score()
        elif self.settings.showme_active is True:
            self.settings.game_active = False
            self.showme_button.draw()
        elif self.settings.message_active is True:
            self.settings.showme_active, self.settings.game_active = False, False
            self._show_final_message()

        pygame.display.flip()

    def _refill_screen(self):
        """ Refill screen to remove killed fleas """
        if self.settings.game_active is True:
            now = pygame.time.get_ticks()
            if now - self.last_refill > self.settings.velocity:
                self.screen.fill(self.settings.play_bg_color)
                self.last_refill = now
        elif self.settings.intro_active is True:
            self.screen.fill(self.settings.bg_color)

    def run_game(self):
        """ Start the main loop for the game """

        while True:
            pytime.Clock().tick(25)
            self.purpy.update()
            self._check_events()
            self._refill_screen()
            self._update_screen()
            self._quit_when_drown()
            self.showme_button.update()



if __name__ == '__main__':
    # Make game instance and run the game
    game = PurpyFleas()
    game.run_game()

