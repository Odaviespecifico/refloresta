import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -120
        self.background = pygame.image.load("assets/background/Menu/Background_Refloresta.png")
        self.background = pygame.transform.scale(self.background, (self.game.DISPLAY_W, self.game.DISPLAY_H))

    def draw_cursor(self):
        self.game.draw_text('►', 20, self.cursor_rect.x, self.cursor_rect.y, self.game.YELLOW)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 70
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 110
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.background, (0, 0))

            self.game.draw_text('REFLORESTA', 40, self.mid_w, self.mid_h - 100, self.game.HIGHLIGHT,)
            self.game.draw_text("Iniciar", 20, self.startx, self.starty,
                                self.game.HIGHLIGHT if self.state == "Start" else self.game.WHITE)
            self.game.draw_text("Opções", 20, self.optionsx, self.optionsy,
                                self.game.HIGHLIGHT if self.state == "Options" else self.game.WHITE)
            self.game.draw_text("Créditos", 20, self.creditsx, self.creditsy,
                                self.game.HIGHLIGHT if self.state == "Credits" else self.game.WHITE)

            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.background, (0, 0))

            self.game.draw_text('Opções', 30, self.mid_w, self.mid_h - 60, self.game.HIGHLIGHT)
            self.game.draw_text("Volume", 25, self.volx, self.voly,
                                self.game.HIGHLIGHT if self.state == "Volume" else self.game.WHITE)
            self.game.draw_text("Controles", 25, self.controlsx, self.controlsy,
                                self.game.HIGHLIGHT if self.state == "Controls" else self.game.WHITE)

            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            pass  # TO-DO: Adicionar menus de volume e controles

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

            self.game.display.blit(self.background, (0, 0))
            self.game.draw_text('Créditos', 30, self.mid_w, self.mid_h - 40, self.game.HIGHLIGHT)
            self.game.draw_text('Feito por Davi 🌿', 20, self.mid_w, self.mid_h + 10, self.game.WHITE)
            self.blit_screen()