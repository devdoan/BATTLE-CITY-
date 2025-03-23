import pygame
import gameconfig as gc
from game_assets import GameAssets
from game import Game
from leveleditor import LevelEditor
from levels import LevelData
from startscreen import StartScreen


class Main:
    def __init__(self):
        #  Chương trình chính của game
        #  Khởi tạo game module và bộ âm thanh cho game
        pygame.init()
        pygame.mixer.init()
        
        # Set up
        self.screen = pygame.display.set_mode((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        pygame.display.set_caption("Battle City BY DevDoan's team")

        self.Clock = pygame.time.Clock()
        self.run = True

        self.assets = GameAssets()
        self.levels = LevelData()

        #  Game Start Screen Object and Check
        self.start_screen = StartScreen(self, self.assets)
        self.start_screen_active = True

        #  Game Object
        self.game_on = False
        self.game = None

        #  Level Editor Loading and Check
        self.level_editor_on = False
        self.level_creator = None

    def run_game(self):
        # VÒng lặp chính của trò chơi
        while self.run:
            self.input()
            self.update()
            self.draw()

    def input(self):
        # Xử lý sự kiện khi game chạy
        #  Event Handler when Game == True
        if self.game_on:
            self.game.input()

        #  Input controls for the start screen
        if self.start_screen_active:
            self.start_screen_active = self.start_screen.input()

        # Input controls for when level creator is running
        if self.level_editor_on:
            self.level_creator.input()

        #  Main Game Controls
        if not self.game_on and not self.level_editor_on and not self.start_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

    def update(self):
        # Caaopj nhật lại các sự kiện trong game và trạng thái của nó
        self.Clock.tick(gc.FPS)

        #  Start Screen updating
        if self.start_screen_active:
            self.start_screen.update()

        #  If game is running, update game
        if self.game_on:
            self.game.update()

        if self.game:
            if self.game.end_game == True:
                self.start_screen = StartScreen(self, self.assets)
                self.start_screen_active = True

                self.game_on = False
                self.game = None

        #  If level editor is on, update level editor
        if self.level_editor_on:
            self.level_creator.update()

        if self.level_creator:
            if self.level_creator.active == False:
                self.start_screen = StartScreen(self, self.assets)
                self.start_screen_active = True

                self.level_editor_on = False
                self.level_creator = None

    def draw(self):
        #VẼ các đối tượng của game lên screen
        
        self.screen.fill(gc.BLACK)

        #  If start_screen_active, draw start screen
        if self.start_screen_active:
            self.start_screen.draw(self.screen)

        #  If game is running, draw game screen
        if self.game_on:
            self.game.draw(self.screen)

        #  if level editor is running, draw to screen
        if self.level_editor_on:
            self.level_creator.draw(self.screen)

        pygame.display.update()

    def start_new_game(self, player1, player2):
        """This method is called from the start screen, and starts the game"""
        self.game_on = True
        self.game = Game(self, self.assets, player1, player2)
        self.start_screen_active = False
        return

    def start_level_creator(self):
        self.level_editor_on = True
        self.level_creator = LevelEditor(self, self.assets)
        self.start_screen_active = False


if __name__=="__main__":
    battleCity = Main()
    battleCity.run_game()
    pygame.quit()