import mediapipe as mp
import cv2
from image_collector import put_cv2_text

def init_gesture_recognizer(model_path): # 初始化手勢辨識模型
    # 不同模型間都有的基礎設定 e.g. 模型路徑
    BaseOptions = mp.tasks.BaseOptions
    # 實際工作的類別
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    # 工作類別的進階設定，每種模型可能不同
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    # 輸入設定，算是進階設定的一個欄位
    VisionRunningMode = mp.tasks.vision.RunningMode
    # 建立檔案與程式碼之間的通道
    with open(model_path, 'rb') as model:
        model_file = model.read()
    # 組合各種設定
    options = GestureRecognizerOptions(
        # base_options=BaseOptions(model_asset_path= model_path), # 使用資料夾路徑開啟
        base_options=BaseOptions(model_asset_buffer= model_file), # 直接讀模型的binary內容
        running_mode=VisionRunningMode.IMAGE)
    return GestureRecognizer.create_from_options(options)
def recognize_gesture(model, cv2_frame): # 使用模型辨識手勢
    # cv2 image -> mediapipe image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2_frame)
    gesture_recognition_result = model.recognize(mp_image)
    top_gesture = gesture_recognition_result.gestures
    if top_gesture: # 判斷是否有辨識出手勢
        top_gesture = top_gesture[0][0]
        return top_gesture.category_name, top_gesture.score
    else: # 沒有辨識出手勢
        return "None", 1.0
def recognize_gesture_realtime(model, camera_id): # 使用攝像頭輸入辨識資料
    window_name = "Recognize Gesture"
    camera = cv2.VideoCapture(camera_id)
    is_recognize = False  # 是否開始辨識 預設為否
    while True:
        is_success, frame = camera.read()
        if is_success:
            show_frame = frame.copy()
            put_cv2_text(show_frame, f"Recognize: {is_recognize}", (25, 50))
            if is_recognize:
                gesture, score = recognize_gesture(model, frame)
                put_cv2_text(show_frame, f"Categry: {gesture} - {round(score*100,2)}%", (25, 75))
                key = cv2.waitKey(100)
            else:
                key = cv2.waitKey(1)
            cv2.imshow(window_name, show_frame)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)
        if key == ord("q") or key == ord("Q"): # 結束
            break
        elif key == ord("a") or key == ord("A"): # 開始
            is_recognize = True
        elif key == ord("z") or key == ord("Z"): # 暫停
            is_recognize = False
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = "gesture_recognizer.task"
    camera_id = 0
    gesture_model = init_gesture_recognizer(model_path)
    recognize_gesture_realtime(gesture_model, camera_id)