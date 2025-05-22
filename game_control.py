# gesture_control.py

import cv2
from pynput.keyboard import Controller
import handtrackingmodule2 as htm
import time

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Initialize hand detector and keyboard controller
detector = htm.handDetector(maxHands=1, detectionCon=0.7, trackCon=0.7)
keyboard = Controller()

time.sleep(2)  # Let the camera warm up

print("[INFO] Starting gesture control. Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        fingers = detector.fingersUp()
        print(f"Fingers: {fingers}")

        # Move forward if index finger is up
        if fingers[1] == 1:
            keyboard.release('s')
            keyboard.press('w')
        else:
            keyboard.release('w')

        # Move backward if index finger is down
        if fingers[1] == 0:
            keyboard.press('s')
        else:
            keyboard.release('s')

        # Turn left if thumb is up
        if fingers[0] == 1:
            keyboard.press('a')
        else:
            keyboard.release('a')

        # Turn right if middle finger is up
        if fingers[2] == 1:
            keyboard.press('d')
        else:
            keyboard.release('d')

    cv2.imshow("Hand Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
