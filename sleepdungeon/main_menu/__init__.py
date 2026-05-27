from ..base.floor import Floor
from ..base.room import Room
from ..base.sprite import Sprite
from ..base.context import Context
from ..base.game_constants import SpriteType
from ..base.inputs import InputEvent
from ..sprites.living_object import LivingObject
from ..sprites.hpup import Hpup
from ..render_context import RenderContext
from ..res import IMG_DIR
from ..base.music_manager import MusicManager
import math

from .menu_font_object import MenuFontObject

import pygame


class MainMenu(Sprite):
    __BASE_BACKGROUND: pygame.Surface = None
    __BACKGROUND: pygame.Surface = None
    __RECT: pygame.Rect = None

    def __init__(self):
        super().__init__()
        self.z_index = 64

        self.btns = [
            MenuFontObject("PLAY", (160, 170), True),
            MenuFontObject("SOUND", (160, 250), True),
            MenuFontObject("EXIT", (160, 330), True),
        ]
        self.initial_ticks = 0
        self.cooldown = 0
        self.selected = 0
        self.sound = True
        self.start = False
        self.exit = False
        self.btns[self.selected].cursor = True

    def update(self, context: Context):
        if self.initial_ticks > 0:
            # Block the menu for the initial five updates
            # This prevents the user from triggering an action when
            # he enters the main menu from a lost fight
            self.initial_ticks -= 1
            return
        if self.cooldown > 0:
            self.cooldown -= context.delta_t
            return

        if self.exit:
            context.change_level = "exit"
            return

        if self.start:
            context.change_level = "00"
            self.start = False
            return

        if context.mouse_click and context.mouse_pos is not None:
            for index, btn in enumerate(self.btns):
                if btn.rect.collidepoint(context.mouse_pos):
                    self.cooldown = 200
                    self.btns[self.selected].cursor = False
                    self.selected = index
                    self.btns[self.selected].cursor = True
                    self._activate_selection(context)
                    return

        for event in context.input_events:
            if event == InputEvent.ATTACK:
                self.cooldown = 200
                self._activate_selection(context)
            elif event == InputEvent.MOVE_DOWN:
                self.cooldown = 200
                self.btns[self.selected].cursor = False
                self.selected += 1
                if self.selected == len(self.btns):
                    self.selected = 0
                self.btns[self.selected].cursor = True

            elif event == InputEvent.MOVE_UP:
                self.cooldown = 200
                self.btns[self.selected].cursor = False
                self.selected -= 1
                if self.selected == -1:
                    self.selected = len(self.btns) - 1
                self.btns[self.selected].cursor = True

    def _activate_selection(self, context: Context):

                # giữ cursor luôn hiện
                self.btns[self.selected].cursor = True

                if self.selected == 0:
                    LivingObject._DROP_HEART_CHANCE = 30
                    Hpup._HEAL = 1
                    self.cooldown = 700
                    self.start = True

                elif self.selected == 1:
                    # SOUND
                    if self.sound:
                        self.btns[self.selected].renew_text("SOUND OFF")
                        self.sound = False
                        MusicManager.set_sound(False)
                    else:
                        self.btns[self.selected].renew_text("SOUND ON")
                        MusicManager.set_sound(True)
                        self.sound = True

                elif self.selected == 2:
                    # EXIT
                    self.cooldown = 700
                    self.exit = True

    @classmethod
    def update_render_context(cls, render_context: RenderContext):
        if not cls.__BASE_BACKGROUND:
            cls.__BASE_BACKGROUND = pygame.image.load(
                IMG_DIR + "menu/overlay.png"
            ).convert_alpha()

        cls.__BACKGROUND = pygame.transform.smoothscale(
            cls.__BASE_BACKGROUND,
            render_context.resolution
        )
        cls.__RECT = pygame.Rect(
            (0, 0),
            render_context.resolution
        )

    @property
    def image(self) -> pygame.Surface:
        return self.__BACKGROUND

    @property
    def rect(self) -> pygame.Rect:
        return self.__RECT

    @property
    def sprite_type(self):
        return SpriteType.PLAYER

    @classmethod
    def create_menu(cls) -> Floor:
        menu = Floor("main_menu")
        menu.menu = True
        room = Room(path = None, name = "main_menu")
        menu.rooms.append(room)
        main_menu = cls()
        room.sprites.append(main_menu)
        for btn in main_menu.btns:
            room.sprites.append(btn)
        room.music = "bosslevelsoundtrack"

        return menu
