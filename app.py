import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque
import cv2 as cv
import mediapipe as mp
from model import KeyPointClassifier
import serial
import time

#Initializing the serial connection with Arduino
ser = serial.Serial('COM3', 9600)

# Intialization of the device
def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args


# Sends Command from the Laptop to Arduino
def Serial_Command(id,prev_selection):
    if id == 0: # Hover Gesture
        a='H'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Hover Gesture")

    if id == 1:  # Move Up Gesture
       a='U'
       if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Move Up Gesture")

    if id == 2:  # Move Down Gesture
        a='D'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Move Down Gesture")

    if id == 3:  # Move Forward Gesture
        a='F'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Move Forward Gesture")

    if id == 4:  # Move Backward Gesture
        a='B'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Move Backward Gesture")

    if id == 5:  # Move Left Gesture
        a='L'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Move Left Gesture")

    if id == 6:  # Move Right Gesture
       a='R'
       if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Move Right Gesture")

    if id == 7:    #Start/Stop
        a='S'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Start/Stop Gesture")
    
    if id == 8:    #Rotate Left
        a='T'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Start/Stop Gesture")

    if id == 9:    #Rotate Right
        a='V'
        if(prev_selection!=a):
            ser.write(a.encode())
            prev_selection=a
            print("Start/Stop Gesture")
            
    return prev_selection

def main():
    # Argument parsing
    args = get_args()
    prev_selection=''

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    # Camera preparation ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Model load #############################################################
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    mpDraw = mp.solutions.drawing_utils
    keypoint_classifier = KeyPointClassifier()

    # Read labels ###########################################################
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    # Coordinate history
    history_length = 16
    point_history = deque(maxlen=history_length)

    # Finger gesture history
    finger_gesture_history = deque(maxlen=history_length)

    mode = 0

    while True:

        # Process Key (ESC: end)
        key = cv.waitKey(10)
        if key == ord('q'):  # Q
            break

        # Camera capture
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        #ledDisplay(10)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                prev_selection=Serial_Command(hand_sign_id,prev_selection)

                point_history.append([0, 0])

                # Finger gesture classification
                finger_gesture_id = 0

                # Calculates the gesture IDs in the latest detection
                finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(
                    finger_gesture_history).most_common()

                # Drawing part
                mpDraw.draw_landmarks(debug_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                debug_image = draw_info_text(
                    debug_image,
                    keypoint_classifier_labels[hand_sign_id]
                )
        else:
            point_history.append([0, 0])

        # Screen reflection
        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def logging_csv(number, mode, landmark_list):
    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        csv_path = 'model/keypoint_classifier/keypoint.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
    return


def draw_info_text(image, hand_sign_text):
    if hand_sign_text != "":
        info_text = hand_sign_text
        cv.putText(image, "Gesture Command: " + info_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
        cv.putText(image, "Gesture Command: " + info_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                   cv.LINE_AA)

    cv.putText(image, "LEFT", (30, 300), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv.putText(image, "RIGHT", (860, 300), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    return image


if __name__ == '__main__':
    main()
