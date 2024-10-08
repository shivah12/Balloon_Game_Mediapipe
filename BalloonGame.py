import cv2
import mediapipe as mp
import numpy as np
import random
import time
from PIL import Image, ImageDraw, ImageFont

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Game settings
balloon_radius = 30
balloon_color = (0, 255, 0)  # Green
balloons = []  # List to store balloon positions and speeds
score = 0  # Score variable
num_balloons = 5  # Number of balloons
game_duration = 0  # Game duration in seconds
start_time = None  # Game start time

# Load Poppins font
font_path = 'Poppins-Regular.ttf'
font_size = 32  # Adjust font size as needed
poppins_font = ImageFont.truetype(font_path, font_size)

def generate_balloon(existing_balloons):
    """Generate a random balloon position and speed, ensuring no overlap with existing balloons."""
    while True:
        x = random.randint(balloon_radius, 640 - balloon_radius)
        y = 480  # Start balloons at the bottom of the screen
        speed = random.uniform(5, 10)  # Increased random speed for balloon movement

        # Check for spacing among balloons
        if all(np.hypot(x - b[0], y - b[1]) > 2 * balloon_radius for b in existing_balloons):
            return [x, y, speed]  # Return as a list

def draw_balloon(frame, position):
    """Draw a balloon on the frame."""
    x, y = int(position[0]), int(position[1])
    cv2.circle(frame, (x, y), balloon_radius, balloon_color, -1)

def detect_balloon_pop(hand_landmarks, balloon_position):
    """Detect if a balloon has been popped by hand gesture."""
    if hand_landmarks:
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x = int(index_tip.x * 640)
        y = int(index_tip.y * 480)
        
        distance = np.hypot(x - balloon_position[0], y - balloon_position[1])
        if distance < balloon_radius:
            return True
    return False

def put_text_with_poppins(frame, text, position, font, color=(255, 255, 255)):
    """Draw text on the frame using the Poppins font with center alignment."""
    # Convert the frame to PIL Image
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)

    # Calculate text size using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # bbox[2] is the right x coordinate, bbox[0] is the left x coordinate
    text_height = text_bbox[3] - text_bbox[1]  # bbox[3] is the bottom y coordinate, bbox[1] is the top y coordinate

    # Center the text
    position = (position[0] - text_width // 2, position[1])  # Center horizontally

    # Draw the text
    draw.text(position, text, font=font, fill=color)
    
    # Convert back to OpenCV format
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def display_start_menu(frame):
    """Display the start menu for selecting game duration."""
    global game_duration
    menu_text = "Press '1' for 10s, '2' for 20s, '3' for 30s"
    frame = put_text_with_poppins(frame, menu_text, (320, 200), poppins_font)  # Center the menu text
    frame = put_text_with_poppins(frame, "Press 'ESC' to exit", (320, 250), poppins_font)  # Center the exit text
    return frame

def display_final_score(score):
    """Display the final score on a black background with center alignment."""
    black_background = np.zeros((480, 640, 3), dtype=np.uint8)
    black_background = put_text_with_poppins(black_background, "Time's Up!", (320, 240), poppins_font)  # Center the text
    black_background = put_text_with_poppins(black_background, f'Final Score: {score}', (320, 300), poppins_font)  # Center the score text
    return black_background

# Main game loop
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    cap = cv2.VideoCapture(0)

    # Create a black background frame
    black_background = np.zeros((480, 640, 3), dtype=np.uint8)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if game_duration == 0:  # Display black background and start menu
            frame = display_start_menu(black_background)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('1'):
                game_duration = 10
                start_time = time.time()
                balloons = [generate_balloon([]) for _ in range(num_balloons)]  # Generate initial balloons
            elif key == ord('2'):
                game_duration = 20
                start_time = time.time()
                balloons = [generate_balloon([]) for _ in range(num_balloons)]  # Generate initial balloons
            elif key == ord('3'):
                game_duration = 30
                start_time = time.time()
                balloons = [generate_balloon([]) for _ in range(num_balloons)]  # Generate initial balloons
            elif key == 27:  # ESC key to exit
                break
        
        else:  # Game is active
            frame = cv2.flip(frame, 1)  # Flip the frame for a mirrored view
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            # Move balloons and check for popping
            for balloon in balloons[:]:
                balloon[1] -= balloon[2]  # Move balloon upwards
                
                if balloon[1] < 0:  # If balloon goes off-screen, remove it
                    balloons.remove(balloon)
                    balloons.append(generate_balloon(balloons))  # Generate a new balloon
                else:
                    draw_balloon(frame, balloon)

                # Check for hand landmarks
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        
                        # Check for balloon pop
                        if detect_balloon_pop(hand_landmarks, (balloon[0], balloon[1])):
                            balloons.remove(balloon)
                            score += 1  # Increase score
                            balloons.append(generate_balloon(balloons))  # Generate a new balloon
                            break  # Exit the loop to avoid modifying the list while iterating

            # Display score
            frame = put_text_with_poppins(frame, f'Score: {score}', (320, 30), poppins_font)  # Center score text

            # Check if time is up
            elapsed_time = time.time() - start_time
            if elapsed_time >= game_duration:
                frame = display_final_score(score)
                cv2.imshow('Balloon Pop Game', frame)
                cv2.waitKey(2000)  # Show final score for 2 seconds
                break  # End the game

        # Show the frame
        cv2.imshow('Balloon Pop Game', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
            break

    cap.release()
    cv2.destroyAllWindows()
