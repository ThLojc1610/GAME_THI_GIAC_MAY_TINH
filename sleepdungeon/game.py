#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from typing import List

from .sprites.camera_overlay import CameraOverlay
from .render_context import RenderContext
from .base.inputs import InputEvent, InputManager
from .base.context import Context
from .base.floor import Floor
from .base.room import Room
from .base.sprite import Sprite
from .base.game_constants import SpriteType
from .level_loader import LevelLoader
from .sprites.sidebar import SideBar
from .base.music_manager import MusicManager
from .main_menu import MainMenu
from .main_menu.pause_menu import PauseMenu


class Game(object):

    def __init__(self, render_context: RenderContext):

        self.running = True

        self.render_context = render_context
        self.input_manager = InputManager()
        self.clock = pygame.time.Clock()

        self.current_floor: Floor = None
        self.current_room: Room = None

        self.floors: List[Floor] = []

        self.context = Context()
        self.context.render_context = self.render_context

        self.sidebar: SideBar = SideBar()

        self.paused = False
        self.camera_overlay: CameraOverlay | None = None
        self.pause_menu: PauseMenu | None = None


    def load(self):

        Sprite._update_render_context(self.render_context)

        menu = MainMenu.create_menu()

        self.floors = LevelLoader().load_levels()
        self.floors.append(menu)

        self.current_floor = menu
        self.current_room = self.current_floor.initial_room

        self.sidebar = SideBar()

        MusicManager.playmusic(self.current_room.music)
        # Khởi tạo overlay camera (dùng gesture từ input_manager)
        self.camera_overlay = CameraOverlay(
        self.input_manager.gesture if hasattr(self.input_manager, "gesture") else None
    )   

        if not self.current_floor.menu:
            self.current_room.sprites.append(self.sidebar)


    def set_floor(self, floor_name):

        was_menu = self.current_floor.menu

        for floor in self.floors:
            if floor.name == floor_name:
                self.current_floor = floor

        if not was_menu and not self.current_floor.menu:

            for player in self.current_room.sprites.find_by_type(SpriteType.PLAYER):
                self.current_floor.take_player_properties(player)

        self.set_room(self.current_floor.initial_room.name)


    def set_room(self, room_name):

        self.current_room = self.current_floor.get_room(room_name)

        MusicManager.playmusic(self.current_room.music)

        self.context.block_doors = True

        if not self.current_floor.menu:
            self.current_room.sprites.append(self.sidebar)


    def pause_game(self):

        if self.paused:
            return

        self.paused = True

        self.pause_menu = PauseMenu()

        self.pause_menu.sound_on = MusicManager._MusicManager__SOUND

        self.current_room.sprites.append(self.pause_menu)

        for btn in self.pause_menu.btns:
            self.current_room.sprites.append(btn)


    def resume_game(self):

        if not self.paused:
            return

        self.paused = False

        if self.pause_menu is not None:

            try:
                self.current_room.sprites.remove(self.pause_menu)
            except ValueError:
                pass

            for btn in self.pause_menu.btns:
                try:
                    self.current_room.sprites.remove(btn)
                except ValueError:
                    pass

        self.pause_menu = None


    def restart_game(self):

        self.resume_game()

        current_music = None

        if self.current_room is not None:
            current_music = self.current_room.music

        # LOAD MENU + LEVELS
        menu = MainMenu.create_menu()

        self.floors = LevelLoader().load_levels()
        self.floors.append(menu)

        # tìm gameplay floor đầu tiên
        for floor in self.floors:
            if floor.name == "00":
                self.current_floor = floor
                break

        self.current_room = self.current_floor.initial_room

        self.sidebar = SideBar()

        if not self.current_floor.menu:
            self.current_room.sprites.append(self.sidebar)

        # chỉ đổi nhạc nếu khác
        if (
            current_music is None
            or self.current_room.music != current_music
        ):
            MusicManager.playmusic(self.current_room.music)

        self.context.change_room = None
        self.context.change_level = None
        self.context.lost = False


    def update(self):

        events = pygame.event.get()

        self.context.mouse_click = False
        self.context.mouse_pos = None

        event_set = self.input_manager.get_events(events)

        # keyboard / controller events
        for event in event_set:

            if event == InputEvent.QUIT:
                self.running = False

            elif event == InputEvent.MENU:

                if self.paused:
                    continue

                if self.current_floor is not None and not self.current_floor.menu:
                    self.pause_game()
                    return

                if self.current_floor is not None and self.current_floor.menu:
                    return


        # mouse + resize
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.context.mouse_click = True
                self.context.mouse_pos = event.pos

            if event.type == pygame.VIDEORESIZE:
                self.render_context.resize(event.dict['size'])
                Sprite._update_render_context(self.render_context)


        # room change
        if self.context.change_room is not None:

            player = self.current_room.remove_player()

            self.set_room(self.context.change_room)

            self.current_room.add_player(player)

            self.context.change_room = None


        # floor change
        if self.context.change_level is not None:

            if self.context.change_level == "exit":
                self.running = False
                return

            self.set_floor(self.context.change_level)

            self.context.change_level = None


        # paused state
        if self.paused:

            if self.pause_menu is None:
                return

            self.context.input_events = event_set
            self.context.sprites = self.current_room.sprites

            self.pause_menu.update(self.context)

            if self.pause_menu is None:
                return


            if self.pause_menu.action == "continue":

                self.resume_game()
                return


            elif self.pause_menu.action == "toggle_sound":

                MusicManager.set_sound(
                    not MusicManager._MusicManager__SOUND
                )

                self.pause_menu.btns[2].renew_text(
                    "SOUND ON"
                    if MusicManager._MusicManager__SOUND
                    else "SOUND OFF"
                )

                self.pause_menu.sound_on = (
                    MusicManager._MusicManager__SOUND
                )

                self.pause_menu.action = None


            elif self.pause_menu.action == "restart":

                self.restart_game()
                return


            elif self.pause_menu.action == "exit":

                self.resume_game()
                self.load()
                self.set_floor("main_menu")

                return


        # normal gameplay
        self.context.input_events = event_set
        self.context.sprites = self.current_room.sprites

        for sprite in self.context.sprites:

            sprite.update(self.context)

            if self.context.lost:

                self.context.lost = False

                self.load()

                self.set_floor("main_menu")

                return


    def render(self):

            self.render_context.screen.fill((200, 200, 100))

            if self.paused:
                sprites_to_draw = self.current_room.sprites
            else:
                sprites_to_draw = self.context.sprites

            for sprite in sprites_to_draw.by_z_index:

                img = sprite.image
                rect = sprite.rect

                if img is None or rect is None:
                    continue

                self.render_context.screen.blit(img, rect)

            # Vẽ camera overlay lên góc dưới-phải (NGOÀI vòng for, cùng cấp với for)
            if self.camera_overlay is not None:
                self.camera_overlay.render(self.render_context.screen)


    def game(self):

        self.load()

        while self.running:

            self.update()

            self.render()

            self.context.delta_t = self.clock.tick(60)

            pygame.display.update()