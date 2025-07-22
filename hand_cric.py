import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import pandas as pd
import multiprocessing
from multiprocessing import Process, Queue
import cv2
import numpy as np
import mediapipe as mp
import sklearn
from sklearn.ensemble import RandomForestClassifier
import pickle
import time

# Load the trained model
with open("rf.pkl", "rb") as f:
    rn = pickle.load(f)

def cricket(index, wind_name, queue):
    vid = cv2.VideoCapture(index)
    hands = mp.solutions.hands
    draw = mp.solutions.drawing_utils
    hand_model = hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.9,
        min_tracking_confidence=0.9
    )

    # Display "Ready to Play" screen
    ready_frame = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.putText(ready_frame, f"{wind_name} - Ready to Play", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
    cv2.imshow(wind_name, ready_frame)
    cv2.waitKey(2000)

    predict = -1
    start_time = time.time()

    while True:
        success, frame = vid.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand_model.process(rgb)

        if result.multi_hand_landmarks:
            draw.draw_landmarks(frame, result.multi_hand_landmarks[0], hands.HAND_CONNECTIONS)
            hand = []
            for i in result.multi_hand_landmarks[0].landmark:
                hand.extend([i.x, i.y, i.z])

            if hand:
                reshape_hand = np.array(hand).reshape(1, -1)
                try:
                    predict = rn.predict(reshape_hand)[0]
                except Exception as e:
                    print(f"[ERROR] Model prediction failed: {e}")
                    predict = -1

                cv2.putText(frame, f"{predict}", (80, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                if predict in [1, 2, 3, 4, 6]:
                    break

        cv2.putText(frame, wind_name, (80, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow(wind_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if time.time() - start_time > 30:
            print(f"[TIMEOUT] No valid hand gesture detected for {wind_name}.")
            predict = -1
            break

    vid.release()
    cv2.destroyWindow(wind_name)
    queue.put(predict)

def toss_coin():
    print("Welcome to Hand Gesture Cricket Game")
    print("Instructions:")
    print("- Two players required with separate webcams")
    print("- Player 1 uses camera index 0, Player 2 uses camera index 1\n")

    player1_name = input("Enter Player 1 name: ").strip()
    player2_name = input("Enter Player 2 name: ").strip()

    start = input("Type 'start' to begin the toss: ").strip().lower()
    if start != "start":
        print("Invalid start input.")
        exit()

    choice = input(f"{player1_name}, choose Heads or Tails: ").strip().lower()
    coin_result = np.random.choice(['heads', 'tails'])
    print(f"Coin tossed: {coin_result}")

    if choice == coin_result:
        print(f"{player1_name} won the toss")
        print("1. Batting\n2. Bowling")
        decision = int(input(f"{player1_name}, choose 1 or 2: "))
        if decision == 1:
            return player1_name, player2_name, "Batting", "Bowling"
        else:
            return player1_name, player2_name, "Bowling", "Batting"
    else:
        print(f"{player2_name} won the toss")
        print("1. Batting\n2. Bowling")
        decision = int(input(f"{player2_name}, choose 1 or 2: "))
        if decision == 1:
            return player1_name, player2_name, "Bowling", "Batting"
        else:
            return player1_name, player2_name, "Batting", "Bowling"

if __name__ == "__main__":
    p1_name, p2_name, p1_role, p2_role = toss_coin()
    p1_score = 0
    p2_score = 0

    print("\nCamera Assignments:")
    print(f"{p1_name} uses camera index 0")
    print(f"{p2_name} uses camera index 1")

    print(f"\n{p1_name} is {p1_role}")
    print(f"{p2_name} is {p2_role}\n")

    for over in range(2):
        print(f"Over {over + 1}")
        for ball in range(6):
            print(f"Ball {ball + 1}")
            q1 = Queue()
            q2 = Queue()

            p1 = Process(target=cricket, args=(0, f"{p1_name} - {p1_role}", q1))
            p2 = Process(target=cricket, args=(1, f"{p2_name} - {p2_role}", q2))

            p1.start()
            p2.start()

            try:
                an1 = q1.get(timeout=15)
            except:
                an1 = -1
            try:
                an2 = q2.get(timeout=15)
            except:
                an2 = -1

            p1.join()
            p2.join()

            print(f"{p1_name} shows: {an1}")
            print(f"{p2_name} shows: {an2}")

            if an1 == -1 or an2 == -1:
                print("One or both players failed to show a valid gesture.")
                continue

            if p1_role == "Batting":
                if an1 == an2:
                    print(f"{p1_name} is OUT!")
                    break
                else:
                    p1_score += an1
            else:
                if an1 == an2:
                    print(f"{p2_name} is OUT!")
                    break
                else:
                    p2_score += an2

        # Swap roles
        p1_role, p2_role = p2_role, p1_role

    print("\nFinal Scores:")
    print(f"{p1_name}: {p1_score}")
    print(f"{p2_name}: {p2_score}")

    if p1_score > p2_score:
        print(f"{p1_name} wins by {p1_score - p2_score} runs.")
    elif p2_score > p1_score:
        print(f"{p2_name} wins by {p2_score - p1_score} runs.")
    else:
        print("Match Drawn.")
