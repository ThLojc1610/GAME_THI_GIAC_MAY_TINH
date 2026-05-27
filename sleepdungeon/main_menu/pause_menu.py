#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional

import pygame

from ..base.context import Context
from ..base.game_constants import SpriteType
from ..base.inputs import InputEvent
from ..base.sprite import Sprite
from ..main_menu.menu_font_object import MenuFontObject
from ..render_context import RenderContext


class PauseMenu(Sprite):
    __BACKGROUND: Optional[pygame.Surface] = None
    __RECT: Optional[pygame.Rect] = None

    def __init__(self):
        super().__init__()
        self.z_index = 96
        self.btns = [
            MenuFontObject("CONTINUE", (145, 150), True),
            MenuFontObject("RESTART", (145, 230), True),
            MenuFontObject("SOUND ON", (145, 310), True),
            MenuFontObject("EXIT", (145, 390), True),
        ]

        self.selected = 0
        self.btns[self.selected].cursor = True
        self.sound_on = True

        self.action: Optional[str] = None
        self.cooldown_ms = 0

        # Ensure menu appears immediately
        for b in self.btns:
            b.blend_in()

    def update(self, context: Context):
        # Block rapid repeats
        if self.cooldown_ms > 0:
            self.cooldown_ms -= context.delta_t
            return

        # Only allow mouse selection (no keyboard navigation)
        if context.mouse_click and context.mouse_pos is not None:
            for index, btn in enumerate(self.btns):
                if btn.rect is not None and btn.rect.collidepoint(context.mouse_pos):
                    self.cooldown_ms = 200
                    self.btns[self.selected].cursor = False
                    self.selected = index
                    self.btns[self.selected].cursor = True
                    self._activate_selection()
                    return

    def _activate_selection(self):

        if self.selected == 0:
            self.action = "continue"

        elif self.selected == 1:
            self.action = "restart"

        elif self.selected == 2:
            self.action = "toggle_sound"

        elif self.selected == 3:
            self.action = "exit"

    @classmethod
    def update_render_context(cls, render_context: RenderContext):
        # Simple dim overlay; keeps look consistent with main menu style.
        cls.__RECT = pygame.Rect((0, 0), render_context.resolution)
        cls.__BACKGROUND = pygame.Surface(render_context.resolution, pygame.SRCALPHA)
        cls.__BACKGROUND.fill((0, 0, 0, 140))

    @property
    def image(self) -> Optional[pygame.Surface]:
        return self.__BACKGROUND

    @property
    def rect(self) -> Optional[pygame.Rect]:
        return self.__RECT
    @property
    def sprite_type(self):
        return SpriteType.GHOST

