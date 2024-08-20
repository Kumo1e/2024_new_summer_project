import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

model_path = r"C:\Users\lenovo\VSC\gesture_recognizer.task"
with open(model_path, 'rb') as model:
    model_file = model.read()

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the image mode:
options = GestureRecognizerOptions(
    # base_options=BaseOptions(model_asset_path= model_path),
    base_options=BaseOptions(model_asset_buffer= model_file),
    running_mode=VisionRunningMode.IMAGE)

with GestureRecognizer.create_from_options(options) as recognizer:

    mp_image = mp.Image.create_from_file('images/victory_2.jpg')
    gesture_recognition_result = recognizer.recognize(mp_image)
    top_gesture = gesture_recognition_result
    hand_landmarks = gesture_recognition_result
    if top_gesture and hand_landmarks:
        top_gesture = top_gesture.gestures[0][0]
        hand_landmarks = hand_landmarks.hand_landmarks[0]
        print(f"Top Gesture: {top_gesture.category_name} {top_gesture.score}")
    # for landmark in hand_landmarks:
    #     print(f"Landmark: {round(landmark.x,3)} {round(landmark.y,3)} {round(landmark.z,3)}")


import cv2
from mediapipe.framework.formats import landmark_pb2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
hand_landmarks_proto.landmark.extend(
    [landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) 
    for landmark in hand_landmarks]
    )

import numpy as np
annotated_image = mp_image.numpy_view()[:,:,::-1].copy()

mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            mp_hands.HAND_CONNECTIONS,
            # mp_drawing_styles.get_default_hand_landmarks_style(),
            # mp_drawing_styles.get_default_hand_connections_style()
            )

cv2.imshow("Hands", annotated_image)
key = cv2.waitKey(20000)
if key == ord("q"):
    cv2.destroyAllWindows()
cv2.destroyAllWindows()