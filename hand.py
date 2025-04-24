import mediapipe as mp
import cv2
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

video_cap = cv2.VideoCapture(0)
click_down = False
while True:
    ret, video_data = video_cap.read()
    video_data = cv2.flip(video_data, 1)
    frame_height, frame_width, _ = video_data.shape
    rgb_frame = cv2.cvtColor(video_data, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #landmark[8] = index finger tip
            index_finger_tip = hand_landmarks.landmark[8]
            #mp_draw.draw_landmarks(video_data, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            #screen coordinates
            index_x = int(index_finger_tip.x * frame_width)
            index_y = int(index_finger_tip.y * frame_height)

            # landmark[4] = Thumb tip
            thumb_tip = hand_landmarks.landmark[4]
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)

            cv2.circle(video_data, (index_x, index_y), 10, (255, 0, 255), -1) #circle on index finger
            cv2.circle(video_data, (thumb_x, thumb_y), 10, (0, 255, 255), -1) #circle on thumb

            # maps to scrn coordinates
            screen_x = int(index_finger_tip.x * screen_width)
            screen_y = int(index_finger_tip.y * screen_height)

            pyautogui.moveTo(screen_x, screen_y)

            #checks the distance , if index and thmb are close enough, it clicks
            distance = math.hypot(thumb_x - index_x, thumb_y - index_y)

            if distance < 40:
                # Click when pinched
                if not click_down:
                    click_down = True
                    pyautogui.click()
                    cv2.putText(video_data, "CLICK", (index_x, index_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                click_down = False  # Reset state

            mp_draw.draw_landmarks(video_data, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    cv2.imshow("Hand Tracking (Quit-q)", video_data)
    #waitKey(1) waits for 1ms and returns the key pressed
    if cv2.waitKey(1) == ord('q'): #ord returns ascii value
        break
    # cv2.imshow("Video_live",video_data)
    # if cv2.waitKey(10) == ord("a"):
    #     break
video_cap.release()