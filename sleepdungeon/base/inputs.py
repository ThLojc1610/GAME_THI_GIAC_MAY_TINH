#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Set, Optional
from enum import Enum

import pygame

try:
    from .gesture_input import GestureInput
    _GESTURE_AVAILABLE = True
except ImportError:
    _GESTURE_AVAILABLE = False
    print("[InputManager] Không tìm thấy gesture_input.py")


class InputEvent(Enum):
    QUIT = 0
    MOVE_UP = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    MOVE_LEFT = 4
    ATTACK = 5
    SWAP = 6
    BOMB = 7
    MENU = 8


class InputManager:

    def __init__(self):
        self.joystick: Optional[pygame.joystick.Joystick] = None

        for j_id in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(j_id)
            joystick.init()
            if joystick.get_numhats() == 0:
                continue
            elif joystick.get_numbuttons() < 4:
                continue
            self.joystick = joystick
            self.joystick.init()
            break

        self.gesture: Optional['GestureInput'] = None
        if _GESTURE_AVAILABLE:
            self.gesture = GestureInput(camera_index=0)
            self.gesture.start()

    def get_events(self, events: list) -> Set['InputEvent']:
        event_set: Set['InputEvent'] = set()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            event_set.add(InputEvent.MOVE_UP)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            event_set.add(InputEvent.MOVE_RIGHT)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            event_set.add(InputEvent.MOVE_DOWN)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            event_set.add(InputEvent.MOVE_LEFT)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    event_set.add(InputEvent.ATTACK)
                elif event.key == pygame.K_e:
                    event_set.add(InputEvent.SWAP)
                elif event.key == pygame.K_q:
                    event_set.add(InputEvent.BOMB)
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                    event_set.add(InputEvent.MENU)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    event_set.add(InputEvent.ATTACK)
                if event.button == 1 or event.button == 2:
                    event_set.add(InputEvent.SWAP)
                if event.button == 3:
                    event_set.add(InputEvent.BOMB)

            elif event.type == pygame.QUIT:
                event_set.add(InputEvent.QUIT)

        if self.joystick is not None:
            (x, y) = self.joystick.get_hat(0)
            if x == -1:
                event_set.add(InputEvent.MOVE_LEFT)
            if x == 1:
                event_set.add(InputEvent.MOVE_RIGHT)
            if y == -1:
                event_set.add(InputEvent.MOVE_DOWN)
            if y == 1:
                event_set.add(InputEvent.MOVE_UP)

            (x, y) = (self.joystick.get_axis(0), -self.joystick.get_axis(1))
            if x < -0.5:
                event_set.add(InputEvent.MOVE_LEFT)
            if x > 0.5:
                event_set.add(InputEvent.MOVE_RIGHT)
            if y < -0.5:
                event_set.add(InputEvent.MOVE_DOWN)
            if y > 0.5:
                event_set.add(InputEvent.MOVE_UP)

        if self.gesture is not None:
            event_set |= self.gesture.get_events()

        return event_set