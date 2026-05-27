#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gesture_input.py - RIGHT HAND ONLY
----------------------------------
- Nắm đấm (không làm gì) → IDLE
- 👆 Giơ ngón trỏ → ATTACK
- 👍 Giơ ngón cái → BOMB
"""

import threading
import time
import math
from typing import Set

try:
    import cv2
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

def _get_input_event():
    from .inputs import InputEvent
    return InputEvent

# ── Hằng số ────────────────────────────────────────────────────────────
GESTURE_HOLD_FRAMES = 1
CAMERA_OVERLAY_WIDTH = 240
CAMERA_OVERLAY_HEIGHT = 180


class GestureInput:
    
    def __init__(self, camera_index: int = 0, width: int = 320, height: int = 240):
        self._camera_index = camera_index
        self._width = width
        self._height = height
        
        self._lock = threading.Lock()
        self._events: Set = set()
        self._running = False
        self._thread = None
        self._overlay_frame = None
        
        self._right_counter = {}
        self._prev_right = "none"
        
        self.available = MEDIAPIPE_AVAILABLE
        
    def start(self):
        if not self.available:
            print("[GestureInput] MediaPipe/OpenCV không khả dụng")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("[GestureInput] Đã khởi động - Tay phải: 👆=ATTACK, 👍=BOMB")
        
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            
    def get_events(self) -> Set:
        with self._lock:
            return set(self._events)
        
    def get_overlay_frame(self):
        with self._lock:
            return self._overlay_frame
            
    def _is_finger_up(self, lm, tip_id, pip_id, mcp_id) -> bool:
        """Kiểm tra ngón tay có duỗi thẳng không"""
        tip = lm.landmark[tip_id]
        pip = lm.landmark[pip_id]
        mcp = lm.landmark[mcp_id]
        
        # Ngón duỗi khi đầu ngón cao hơn đốt giữa
        return tip.y < pip.y and tip.y < mcp.y
        
    def _classify_right_hand(self, lm) -> str:
        # Kiểm tra các ngón
        thumb_up = self._is_finger_up(lm, 4, 3, 2)    # Ngón cái
        index_up = self._is_finger_up(lm, 8, 6, 5)    # Ngón trỏ
        middle_up = self._is_finger_up(lm, 12, 10, 9) # Ngón giữa
        ring_up = self._is_finger_up(lm, 16, 14, 13)  # Ngón áp út
        pinky_up = self._is_finger_up(lm, 20, 18, 17) # Ngón út
        
        # 👆 ATTACK: CHỈ ngón trỏ duỗi (các ngón khác nắm)
        if index_up and not thumb_up and not middle_up and not ring_up and not pinky_up:
            return "attack"
        
        # 👍 BOMB: CHỈ ngón cái duỗi (các ngón khác nắm)
        if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
            return "bomb"
        
        # Nắm đấm (không có ngón nào duỗi) → none
        return "none"
        
    def _debounce_right(self, gesture: str) -> str:
        if gesture == self._prev_right and gesture != "none":
            self._right_counter[gesture] = self._right_counter.get(gesture, 0) + 1
        else:
            self._right_counter.clear()
            if gesture != "none":
                self._right_counter[gesture] = 1
            self._prev_right = gesture
            
        if self._right_counter.get(gesture, 0) >= GESTURE_HOLD_FRAMES:
            return gesture
        return "none"
        
    def _update_events(self, right: str):
        InputEvent = _get_input_event()
        events = set()
        
        if right == "attack":
            events.add(InputEvent.ATTACK)
        elif right == "bomb":
            events.add(InputEvent.BOMB)
            
        with self._lock:
            self._events = events
            
    def _draw_hud(self, frame, right: str):
        h, w = frame.shape[:2]
        
        def put(text, x, y, color=(0, 255, 0)):
            cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
        
        put(f"RIGHT HAND: {right}", 10, 25, (255, 100, 0))
        
    def _run(self):
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        
        cap = cv2.VideoCapture(self._camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
        
        if not cap.isOpened():
            print("[GestureInput] Không mở được camera!")
            return
        
        with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.4,
            model_complexity=0,
        ) as hands:
            
            while self._running:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.01)
                    continue
                    
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)
                
                right_gesture = "none"
                
                if result.multi_hand_landmarks and result.multi_handedness:
                    for lm, handedness in zip(result.multi_hand_landmarks,
                                               result.multi_handedness):
                        label = handedness.classification[0].label
                        if label == "Right":
                            mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
                            right_gesture = self._classify_right_hand(lm)
                            
                right_stable = self._debounce_right(right_gesture)
                self._update_events(right_stable)
                self._draw_hud(frame, right_stable)
                
                overlay = cv2.resize(frame, (CAMERA_OVERLAY_WIDTH, CAMERA_OVERLAY_HEIGHT),
                                    interpolation=cv2.INTER_NEAREST)
                with self._lock:
                    self._overlay_frame = overlay
                    
        cap.release()