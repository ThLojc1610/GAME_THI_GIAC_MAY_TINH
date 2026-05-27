from ..base.sprite import Sprite
from ..base.context import Context
from ..base.game_constants import SpriteType
from ..render_context import RenderContext
from ..res import FONT_DIR
from typing import Dict, List

from enum import Enum
import pygame

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ >ÂĂĐÊÔƠƯẠẢẦẤẦIÃÒẪŨỤỲỴÍẾỂỂỒỜỜƯ" 


class MenuFontState(Enum):
    INVISIBLE = 1
    BLEND_IN = 2
    VISIBLE = 3
    BLEND_OUT = 4

class MenuFontObject(Sprite):
    __GLYPHS: Dict[str, pygame.Surface] = {}
    __FONT: pygame.font.Font = None
    _WIDTH = 0
    _ANIMATION_LENGTH = 500
    _HEIGHT = 0

    def __init__(self, text: str, pos: List[int], visible = False):
        super().__init__()
        self.z_index = 128
        self.text = text
        self.new_text = None
        self.pos = pos
        self.state = MenuFontState.VISIBLE if visible else MenuFontState.INVISIBLE
        self.cursor = False
        self.animation_t = 0
        self.glyph_delay = self._ANIMATION_LENGTH / len(text) * .7
        self.glyph_period = self._ANIMATION_LENGTH / len(text) * (1/.7)

    def blend_in(self):
        self.animation_t = 0
        self.state = MenuFontState.BLEND_IN

    def blend_out(self):
        self.animation_t = 0
        self.state = MenuFontState.BLEND_OUT

    def renew_text(self, text):
        if self.state == MenuFontState.VISIBLE:
            self.animation_t = 0
            self.state = MenuFontState.BLEND_OUT
            self.new_text = text
        else:
            self.text = text

    def update(self, context: Context):
        if self.state == MenuFontState.BLEND_IN:
            self.animation_t += context.delta_t
            if self.animation_t > self._ANIMATION_LENGTH:
                self.animation_t = 0
                self.state = MenuFontState.VISIBLE
        if self.state == MenuFontState.BLEND_OUT:
            self.animation_t += context.delta_t
            if self.animation_t > self._ANIMATION_LENGTH:
                self.animation_t = 0
                if self.new_text is not None:
                    self.state = MenuFontState.BLEND_IN
                    self.text = self.new_text
                    self.new_text = None
                else:
                    self.state = MenuFontState.INVISIBLE

    @classmethod
    def update_render_context(cls, render_context: RenderContext):
        cls.__FONT = pygame.font.Font(
            FONT_DIR + "Game_font.ttf",
            int(cls.tile_size * 1)
        )

        cls._WIDTH = render_context.resolution[0]
        cls._HEIGHT = cls.__FONT.size(CHARSET)[1]

        for c in CHARSET:
            cls.__GLYPHS[c] = cls.__FONT.render(c, True, (255, 255, 255))

    @property
    def image(self) -> pygame.Surface:
        if self.state == MenuFontState.INVISIBLE:
            return None

        text = ("> " + self.text) if self.cursor else self.text
        text_width, text_height = self.__FONT.size(text)
        width = int(text_width + 20 * self.scaling)
        height = int(text_height + 10 * self.scaling)

        img = pygame.Surface((width, height), pygame.SRCALPHA)
        img.fill((0, 0, 0, 0))

        x_offset = int(10 * self.scaling)
        y_offset = int((height - text_height) / 2)
        x = x_offset

        for c in text.upper():

            glyph = self.__GLYPHS.get(c)

            if glyph is not None:
                img.blit(glyph, (x, y_offset))

            x += self.__FONT.size(c)[0]

        return img

    @property
    def rect(self) -> pygame.Rect:
        text = ("> " + self.text) if self.cursor else self.text
        text_width, text_height = self.__FONT.size(text)
        x = int(self.pos[0] * self.scaling)
        y = int(self.pos[1] * self.scaling)
        width = int(text_width + 20 * self.scaling)
        height = int(text_height + 10 * self.scaling)
        return pygame.Rect(
            x,
            y,
            width,
            height
        )

    @property
    def sprite_type(self):
        return SpriteType.GHOST
