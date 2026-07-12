import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize webcam
cap = cv2.VideoCapture(0)

# PyAutoGUI fail-safe 
# (CRITICAL: Move your mouse to the top-left corner of your screen to emergency-stop the script!)
pyautogui.FAILSAFE = True 

print("Cygnus Airtouch is running in the background...")
print("To stop it, press Ctrl+C in this command prompt window, or move your mouse to the extreme top-left corner.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally for mirror mapping
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Convert BGR to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract specific finger tip coordinates
            index_tip = hand_landmarks.landmark[8]    # Index Finger Tip
            middle_tip = hand_landmarks.landmark[12]  # Middle Finger Tip

            # Convert normalized coordinates to pixel values
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            middle_x, middle_y = int(middle_tip.x * w), int(middle_tip.y * h)

            # Map coordinates to screen size
            screen_x = int(index_tip.x * screen_width)
            screen_y = int(index_tip.y * screen_height)

            # Move mouse cursor
            pyautogui.moveTo(screen_x, screen_y)

            # --- Gesture for Clicking ---
            distance = ((index_x - middle_x) ** 2 + (index_y - middle_y) ** 2) ** 0.5
            if distance < 40:  
                pyautogui.click()
                pyautogui.sleep(0.2)

    # Note: cv2.imshow has been completely removed so no window pops up.
    # We still keep a tiny waitKey pause so the loop processes smoothly
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
          
