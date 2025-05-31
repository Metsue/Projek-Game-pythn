import cv2
import pyautogui
import numpy as np
import webbrowser
import time
import mediapipe as mp
import threading
import math

# Buka Geometry Dash
def buka_game():
    url = "https://geometrydashlitepc.io/"
    webbrowser.open(url)

threading.Thread(target=buka_game).start()
time.sleep(15)

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam
vid = cv2.VideoCapture(0)

JARAK_BUKA = 60
last_jump_time = 0
JUMP_INTERVAL = 0.15  # lompat tiap 150ms saat dibuka

while True:
    success, frame = vid.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = handLms.landmark
            tip_index = (int(lm_list[8].x * w), int(lm_list[8].y * h))
            tip_thumb = (int(lm_list[4].x * w), int(lm_list[4].y * h))

            # Gambar jari
            cv2.circle(frame, tip_index, 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, tip_thumb, 10, (0, 255, 255), cv2.FILLED)
            cv2.line(frame, tip_index, tip_thumb, (0, 255, 0), 3)

            # Hitung jarak
            jarak = math.hypot(tip_index[0] - tip_thumb[0], tip_index[1] - tip_thumb[1])
            cv2.putText(frame, f"Jarak: {int(jarak)}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Selama dibuka, lompat terus
            now = time.time()
            if jarak > JARAK_BUKA and now - last_jump_time > JUMP_INTERVAL:
                pyautogui.press('space')
                print("Lompat terus!")
                last_jump_time = now

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, "Coding Is Fun jer indra", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow("YIIIIIIIIHAHAAA INDRAAA", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
