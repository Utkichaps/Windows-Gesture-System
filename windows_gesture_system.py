
from unittest import result
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=1,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()

    x , y, c = image.shape

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)    
    print('Handedness:', results.multi_handedness)
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
      print("-----------")

      landmarks = []
      for hand_landmarks in results.multi_hand_landmarks:      

        for lm in hand_landmarks.landmark:
              # print(id, lm)
              lmx = int(lm.x * x)
              lmy = int(lm.y * y)
              landmarks.append([lmx, lmy])
        print(len(landmarks))
        print(landmarks)

        image_height, image_width, _ = image.shape
        index_tip_pos = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 100, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 100))
        thumb_tip_pos = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * 100, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * 100))
        dist = np.linalg.norm(index_tip_pos-thumb_tip_pos)
        # print(dist)

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

cv2.destroyAllWindows()