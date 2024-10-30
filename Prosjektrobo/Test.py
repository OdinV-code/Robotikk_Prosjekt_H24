from djitellopy import Tello
import cv2
import pygame
import time

# Initialize pygame
pygame.init()



# Initialize the Tello drone
drone = Tello()
drone.connect()
battery_level = drone.get_battery()

# Start video stream
drone.streamon()

# Pygame window setup
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Tello Drone Control")

# Control variables
speed = 50  # Speed for movement commands
is_flying = False  # Flag to ensure the drone stays on the ground initially

# Function to handle keypresses for drone control
def handle_keys():
    if not is_flying:
        return  # Skip controls if the drone has not taken off

    # Initialize movement variables
    lr = 0  # Left/Right movement
    fb = 0  # Forward/Backward movement
    ud = 0  # Up/Down movement
    yaw = 0  # Yaw/rotation

    keys = pygame.key.get_pressed()

    # Forward and backward
    if keys[pygame.K_w]:
        fb = speed  # Forward
    elif keys[pygame.K_s]:
        fb = -speed  # Backward

    # Left and right
    if keys[pygame.K_a]:
        lr = -speed  # Left
    elif keys[pygame.K_d]:
        lr = speed  # Right

    # Up and down
    if keys[pygame.K_SPACE]:
        ud = speed  # Up
    elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
        ud = -speed  # Down

    # Rotate left and right
    if keys[pygame.K_LEFT]:
        yaw = -speed  # Rotate left
    elif keys[pygame.K_RIGHT]:
        yaw = speed  # Rotate right

    # Send the control command to the drone
    drone.send_rc_control(lr, fb, ud, yaw)

# Main loop
try:
    while True:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if is_flying:
                    drone.land()  # Land the drone if the window is closed and it's flying
                pygame.quit()
                cv2.destroyAllWindows()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and is_flying:
                    drone.land()  # Land the drone if Escape is pressed
                    is_flying = False
                    print("Landing...")
                elif event.key == pygame.K_RETURN and not is_flying:  # Enter key for takeoff
                    drone.takeoff()
                    is_flying = True
                    print("Taking off...")

        handle_keys()  # Call the function to handle key presses

        # Get the frame from the drone
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        
        cv2.putText(
        img, 
        f"Battery: {battery_level}%", 
        (10, 30), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (0, 255, 0),  # Green color
        2
        )


        # Display the video feed
        cv2.imshow("Live Feed", img)
        
        # Refresh rate for display and keyboard handling
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.05)  # Add a small delay to prevent spamming commands

except KeyboardInterrupt:
    # Safely land the drone if interrupted
    if is_flying:
        drone.land()








# Cleanup
drone.streamoff()
cv2.destroyAllWindows()
pygame.quit()
