#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
camera_overlay.py
-----------------
Hiển thị camera + trạng thái TAY PHẢI
"""

import pygame
import numpy as np

try:
    import cv2
    _CV2_OK = True
except ImportError:
    _CV2_OK = False

# Kích thước overlay
OVERLAY_W = 240
OVERLAY_H = 180
PADDING = 10

# Màu sắc
COLOR_BG = (10, 10, 10, 180)
COLOR_BORDER = (80, 200, 120)
COLOR_RIGHT = (255, 160, 50)

# Map cử chỉ sang text
_GESTURE_TEXT = {
    "attack": " ATTACK",
    "bomb": " BOMB",
    "none": " IDLE",
}


class CameraOverlay:

    def __init__(self, gesture_input=None):
        self._gesture = gesture_input
        self._font_sm = None
        self._bg_surface = None

    def render(self, screen: pygame.Surface):
        if self._gesture is None or not self._gesture.available:
            return

        self._init_fonts()

        frame = self._gesture.get_overlay_frame()
        sw, sh = screen.get_size()

        x = sw - OVERLAY_W - PADDING
        y = sh - OVERLAY_H - PADDING - 30

        bg = self._get_bg()
        screen.blit(bg, (x - 4, y - 4))

        if frame is not None and _CV2_OK:
            cam_surf = self._frame_to_surface(frame)
            screen.blit(cam_surf, (x, y))
        else:
            placeholder = pygame.Surface((OVERLAY_W, OVERLAY_H))
            placeholder.fill((30, 30, 30))
            screen.blit(placeholder, (x, y))

        pygame.draw.rect(screen, COLOR_BORDER,
                         pygame.Rect(x - 1, y - 1, OVERLAY_W + 2, OVERLAY_H + 2), 2)

        right_g = getattr(self._gesture, "_prev_right", "none")
        right_text = f"RIGHT: {_GESTURE_TEXT.get(right_g, right_g)}"
        surf_right = self._font_sm.render(right_text, True, COLOR_RIGHT)

        text_y = y + OVERLAY_H + 5
        screen.blit(surf_right, (x, text_y))

    def _init_fonts(self):
        if self._font_sm is None:
            pygame.font.init()
            self._font_sm = pygame.font.SysFont("segoeui", 14)

    def _get_bg(self) -> pygame.Surface:
        if self._bg_surface is None:
            w = OVERLAY_W + 8
            h = OVERLAY_H + 8 + 30
            self._bg_surface = pygame.Surface((w, h), pygame.SRCALPHA)
            self._bg_surface.fill(COLOR_BG)
        return self._bg_surface

    def _frame_to_surface(self, frame) -> pygame.Surface:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surf = pygame.surfarray.make_surface(np.transpose(rgb, (1, 0, 2)))
        return surf