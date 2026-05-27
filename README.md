# 🎮 SleepDungeon

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Pygame-2D_Game-green?style=for-the-badge&logo=pygame">
  <img src="https://img.shields.io/badge/OpenCV-Computer_Vision-red?style=for-the-badge&logo=opencv">
  <img src="https://img.shields.io/badge/MediaPipe-Gesture_Control-orange?style=for-the-badge">
</p>

---

# 📌 Giới thiệu

**SleepDungeon** là game mê cung hành động 2D được phát triển bằng **Python + Pygame**, kết hợp với công nghệ nhận diện cử chỉ tay thông qua **OpenCV** và **MediaPipe**.

Người chơi sẽ khám phá các căn phòng trong dungeon, chiến đấu với quái vật, né bẫy và tìm đường sống sót.

Điểm nổi bật của game là:
- 🎮 Gameplay dungeon crawler
- ✋ Điều khiển bằng gesture realtime
- 📷 Tích hợp webcam
- 💣 Bom, chiến đấu và bẫy
- 🎵 Âm thanh và hiệu ứng

---

# ✨ Tính năng nổi bật

## 🎮 Gameplay
- Di chuyển trong mê cung
- Chuyển phòng qua hệ thống cửa
- Đặt bom phá vật cản
- Chiến đấu với quái vật
- Né tránh bẫy xoay

## 🧠 Gesture Control
- Điều khiển hành động bằng cử chỉ tay
- Nhận diện gesture realtime bằng webcam
- Kết hợp OpenCV + MediaPipe Hands

## 🎨 Đồ họa & UI
- Pixel art 2D
- Sidebar hiển thị thông tin
- Animation nhân vật và enemy
- Pause menu
- Main menu

## 🔊 Âm thanh
- Nhạc nền
- Hiệu ứng chiến đấu
- Sound menu riêng

---

# 🛠️ Công nghệ sử dụng

| Công nghệ | Vai trò |
|-----------|----------|
| Python | Ngôn ngữ chính |
| Pygame | Engine game 2D |
| OpenCV | Xử lý webcam |
| MediaPipe | Nhận diện bàn tay |
| NumPy | Xử lý dữ liệu |

---

# 📂 Cấu trúc project

```bash
sleepdungeon/
│
├── base/                  # Core game system
├── main_menu/             # Menu chính và pause menu
├── levels/                # Dữ liệu map
├── sprites/               # Hình ảnh nhân vật, quái vật
├── res/                   # Âm thanh, font, texture
│
├── game.py                # Game loop chính
├── level_loader.py        # Load màn chơi
├── render_context.py      # Render game
├── gesture_input.py       # Xử lý cử chỉ tay
└── main.py                # Chạy game
```

---

# ⚙️ Cài đặt

## 1️⃣ Clone project

```bash
git clone https://github.com/ThLojc1610/sleepdungeon.git
cd sleepdungeon
```

---

## 2️⃣ Cài thư viện

```bash
pip install pygame opencv-python mediapipe numpy
```

---

# ▶️ Chạy game

```bash
python -m sleepdungeon
```

---

# 🎮 Điều khiển

## ⌨️ Bàn phím

| Phím | Chức năng |
|------|------------|
| W | Di chuyển lên |
| S | Di chuyển xuống |
| A | Di chuyển trái |
| D | Di chuyển phải |
| ESC | Pause game |

---

## ✋ Gesture Control

| Cử chỉ | Hành động |
|--------|------------|
| 👆 Giơ ngón trỏ | ATTACK |
| 👍 Giơ ngón cái | BOMB |

---

# 📷 Gesture Recognition System

Game sử dụng:
- OpenCV để lấy dữ liệu webcam
- MediaPipe Hands để detect bàn tay
- Xử lý realtime theo từng frame

Ví dụ luồng xử lý:

```python
capture webcam
→ detect hand landmarks
→ recognize gesture
→ convert to game action
→ execute in game
```

---

# 🗺️ Gameplay

## 🏠 Main Menu
- Play
- Sound ON/OFF
- Exit

## ⚔️ Trong game
- Di chuyển qua dungeon
- Tiêu diệt quái vật
- Đặt bom
- Né bẫy xoay
- Thu thập item

---

# 🧱 Hệ thống game

## 👾 Enemy
- AI di chuyển cơ bản
- Có animation
- Có va chạm và damage

## 💣 Bomb
- Đặt bom theo gesture
- Gây sát thương vùng
- Phá vật cản

## 🚪 Room System
- Chuyển phòng qua cửa
- Load map động

---

# 🚀 Hướng phát triển

- Multiplayer
- Boss fight
- Skill system
- Save/Load game
- Inventory
- Enemy AI nâng cao
- Gesture movement hoàn chỉnh
- Leaderboard

---

# 🧪 Ý tưởng học thuật

Project phù hợp để:
- Học lập trình game với Pygame
- Nghiên cứu Computer Vision
- Tìm hiểu Human-Computer Interaction
- Thực hành xử lý ảnh realtime

---
