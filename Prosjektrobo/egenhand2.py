from djitellopy import Tello
import cv2
import mediapipe as mp

# Initialize and connect to the drone
drone = Tello()
drone.connect()
print("Battery:", drone.get_battery(), "%")
drone.streamon()

#init Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

# Display video feed
while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Live Feed", img)
    RGB_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmark_8 = hand_landmarks.landmark[8]
            h, w, _ = img.shape  # Get image dimensions

            # Convert normalized coordinates to pixel coordinates
            x, y = int(landmark_8.x * w), int(landmark_8.y * h)

            # Print the pixel coordinates of landmark 8
            print(f"Landmark 8 (Index Finger Tip): x={x}, y={y}")
            mp_drawing.draw_landmarks(img, hand_landmarks,mp_hands.HAND_CONNECTIONS)

    cv2.imshow("livetrack", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
drone.streamoff()
