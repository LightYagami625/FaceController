import cv2
import mediapipe as mp
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from math import hypot
import numpy as np
import speech_recognition as sr

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get volume range
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

video_cap = cv2.VideoCapture(0)
while True:
    ret, video_data = video_cap.read()
    video_data = cv2.flip(video_data, 1)
    rgb_frame = cv2.cvtColor(video_data, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(video_data, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of thumb tip and index finger tip
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            h, w, _ = video_data.shape
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Draw circles on thumb and index finger tips
            cv2.circle(video_data, (thumb_x, thumb_y), 10, (255, 0, 0), -1)
            cv2.circle(video_data, (index_x, index_y), 10, (255, 0, 0), -1)
            cv2.line(video_data, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)

            # Calculate the distance between thumb and index finger
            distance = hypot(index_x - thumb_x, index_y - thumb_y)

            # Map the distance to the volume range
            vol = np.interp(distance, [20, 200], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)

            # Display the volume level on the screen
            vol_bar = np.interp(distance, [20, 200], [400, 150])
            cv2.rectangle(video_data, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(video_data, (50, int(vol_bar)), (85, 400), (255, 0, 0), -1)

    cv2.imshow("Video_Live", video_data)
    if cv2.waitKey(10) == ord("a"):
        break

video_cap.release()
cv2.destroyAllWindows()
