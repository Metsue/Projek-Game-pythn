#Copyright code by Metsue (Indraa)
#Jangan lupa tag ig @mhmmd_.indra

import cv2
import pyautogui
import numpy as np
import webbrowser
import time
import mediapipe as mp
import threading
import math

# Buka game Subway Surfers
def buka_game():
    url = "https://poki.com/id/g/subway-surfers"
    webbrowser.open(url)

threading.Thread(target=buka_game).start()
time.sleep(15)

# MediaPipe init
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam
vid = cv2.VideoCapture(0)

# Cooldown
last_action_time = 0
COOLDOWN = 0.6

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# BALIK ARAH gesture
def get_direction(tip_index, tip_thumb, h, w):
    dx = tip_index[0] - tip_thumb[0]
    dy = tip_index[1] - tip_thumb[1]

    if abs(dx) > abs(dy):
        if dx > 60:
            return 'right'  # sebelumnya 'left'
        elif dx < -60:
            return 'left'   # sebelumnya 'right'
    else:
        if dy > 80:
            return 'down'  # sebelumnya 'up'
        elif dy < -60:
            return 'up'    # sebelumnya 'down'
    return 'neutral'

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

            cv2.circle(frame, tip_index, 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, tip_thumb, 10, (0, 255, 255), cv2.FILLED)
            cv2.line(frame, tip_index, tip_thumb, (0, 255, 0), 3)

            gesture = get_direction(tip_index, tip_thumb, h, w)

            now = time.time()
            if gesture != 'neutral' and now - last_action_time > COOLDOWN:
                pyautogui.press(gesture)
                print("Gesture:", gesture)
                last_action_time = now

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, "Indra Jago Anjay", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow("Gesture Terbalik Subway Surfers", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
