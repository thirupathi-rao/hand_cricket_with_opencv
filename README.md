# hand_cricket_with_opencv
Great! Based on your project and the images you uploaded (`c1.jpeg` to `c6.jpeg`), here’s a **complete documentation PDF** that includes:

---

### ✅ Contents:

1. **Project Title & Description**
2. **Rules of the Game (with your hand images)**
3. **Player Roles & Flow**
4. **How to Play**
5. **Disclaimer**

---

### 📄 Documentation Preview:

---

# Hand Gesture Based Hand Cricket Game

*A Personal Project using OpenCV, Python & Machine Learning*

---

## 🎮 Overview:

This project is a computer vision-based implementation of the classic hand-cricket game using Python and OpenCV. It allows two players to simulate the game using **hand gestures** that represent runs.

---

## 🧠 Game Rules:

Each hand gesture corresponds to a run:

| Run            | Gesture                        |
| -------------- | ------------------------------ |
| 1 Run          | ![1 Run](attachment\:c1.jpeg)  |
| 2 Runs         | ![2 Runs](attachment\:c2.jpeg) |
| 3 Runs         | ![3 Runs](attachment\:c3.jpeg) |
| 4 Runs         | ![4 Runs](attachment\:c4.jpeg) |
| 6 Runs (Thumb) | ![6 Runs](attachment\:c6.jpeg) |

**OUT Rule:**
If **batter** and **bowler** show the same gesture in the same round → **Batter is OUT**.
The batter’s total score is recorded.

---

## 👥 Player Setup:

* **Player 1**: You can choose to **bat** or **bowl** after toss.
* **Player 2**: Takes the other role.

---

## 🏏 Game Flow:

1. **Start the game**: Type `"start"` when prompted.
2. **Toss**: Choose **Heads or Tails**.
3. **Choose Role**: Winner of toss selects to **bat or bowl**.
4. **Rounds**: Each player shows a hand gesture in front of the webcam.
5. **OUT Detection**: If same score from both players → Out.
6. **Switch Roles**: After one player gets out, roles are swapped.
7. **Win Check**: Player with higher score wins.

---

## 🧪 Tech Stack:

* Python
* OpenCV
* TensorFlow Lite
* Multiprocessing
* Hand Gesture Classification Model

---

## ⚠️ Disclaimer:

This is a **personal project** developed for learning and entertainment purposes. It is **not intended for professional use** or commercial deployment.

---

## 📌 Notes:

* A **10-second timeout** is implemented: If no hand is detected within the time, the game proceeds to the next input.
* A **“Ready to Play”** screen is shown before the game starts using OpenCV overlays.

---

Would you like me to export this as a **PDF** with the images included and properly embedded for upload/sharing?
