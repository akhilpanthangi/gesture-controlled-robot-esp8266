import time

import cv2
import mediapipe as mp
import requests


# ESP8266 robot address and exact firmware endpoints
ROBOT_URL = "http://192.168.4.1"
COMMAND_ENDPOINTS = {
    "forward": "forward",
    "backward": "back",
    "left": "left",
    "right": "right",
    "stop": "stop",
}

# Control settings
STABLE_FRAMES = 5
REQUEST_TIMEOUT = 1
REQUEST_ATTEMPTS = 2
RETRY_INTERVAL = 0.5


def send_command(command, attempts=REQUEST_ATTEMPTS):
    """Send one movement command and return True when the ESP8266 confirms it."""
    endpoint = COMMAND_ENDPOINTS[command]
    command_url = f"{ROBOT_URL}/{endpoint}"

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(command_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            print("Command:", command, " Response:", response.text)
            return True
        except requests.RequestException as error:
            if attempt < attempts:
                time.sleep(0.1)
            else:
                print("Robot not reachable:", error)

    return False


def main():
    # MediaPipe setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )
    mp_draw = mp.solutions.drawing_utils

    # Camera setup
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    tip_ids = [4, 8, 12, 16, 20]
    last_sent_command = None
    candidate_command = "stop"
    stable_count = 0
    next_retry_time = 0.0

    try:
        if not cap.isOpened():
            raise RuntimeError("Could not open the webcam")

        while True:
            success, img = cap.read()
            if not success:
                print("Camera frame unavailable. Stopping the robot.")
                break

            # Mirror the camera so hand movement matches the displayed direction.
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            command = "stop"

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                height, width, _ = img.shape
                landmark_list = []

                for landmark in hand.landmark:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    landmark_list.append((x, y))

                # Finger detection
                fingers = []

                # Thumb
                if landmark_list[tip_ids[0]][0] > landmark_list[tip_ids[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Index, middle, ring and little fingers
                for finger_index in range(1, 5):
                    tip = tip_ids[finger_index]
                    if landmark_list[tip][1] < landmark_list[tip - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = fingers.count(1)
                wrist_x = landmark_list[0][0]
                index_x = landmark_list[8][0]
                horizontal_difference = index_x - wrist_x

                # Gesture logic
                if total_fingers == 0:
                    command = "backward"
                elif horizontal_difference > 100:
                    command = "right"
                elif horizontal_difference < -100:
                    command = "left"
                else:
                    command = "forward"

                mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            # Gesture stability filter
            if command == candidate_command:
                stable_count += 1
            else:
                candidate_command = command
                stable_count = 1
                next_retry_time = 0.0

            current_time = time.monotonic()

            # Send a new stable command. If sending fails, retry after a short delay.
            if (
                stable_count >= STABLE_FRAMES
                and command != last_sent_command
                and current_time >= next_retry_time
            ):
                if send_command(command):
                    last_sent_command = command
                    next_retry_time = 0.0
                else:
                    next_retry_time = current_time + RETRY_INTERVAL

            cv2.putText(
                img,
                "Command: " + command,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Gesture Robot Control", img)

            # Esc closes the program. The finally block sends STOP first.
            if cv2.waitKey(1) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Controller interrupted by user.")
    except RuntimeError as error:
        print(error)
    finally:
        print("Stopping robot and closing the controller...")
        send_command("stop", attempts=3)
        cap.release()
        hands.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
