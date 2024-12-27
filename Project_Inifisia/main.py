print("Starting Imports...", end="", flush=True)
import cv2
import numpy
import ctypes
import hands
from detect_gesture import detect_gesture
from var_config import video, debug

# from cursor import get_cursor_position
SetCursorPos = ctypes.windll.user32.SetCursorPos
del ctypes
print("\r\033[5A\033[KImports Done.")
if video:
    video_capture = cv2.VideoCapture(video)
else:
    video_capture = cv2.VideoCapture(0)

frame_count = 0
if not video_capture.isOpened():
    if video:
        print("Error: Could not open video.")
    else:
        print("Error: Couldn't Access Camera.")
    exit()
screen_height, screen_width = 1366, 768


def put_text(img_frame, gesture_words):
    img_h_, img_w_, _ = img_frame.shape
    x, y = 10, img_h_ - 10
    for i, word in enumerate(gesture_words):
        (w, h), _ = cv2.getTextSize(word, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        if y < h + 10:
            break
        cv2.putText(img_frame, word, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0x00, 0xFF), 2)
        y -= h + 10
    return img_frame


while True:
    try:
        ret, frame = video_capture.read()
        frame_count += 1
        if not ret:
            print("\nEnd of video or cannot read the frame.")
            break
        landmarks = hands.detect_hands(frame)
        detected_gestures = [detect_gesture(landmarks=i) for i in landmarks]
        frame = put_text(frame, detected_gestures)

        height, width, _ = frame.shape
        if len(landmarks) == 1:
            if detected_gestures[0] == "Pointing Upwards":  # Move Cursor along with the Tip of the Fore Finger
                cur_pos = numpy.array(landmarks[0][8][0:2]) * numpy.array([screen_height, screen_width]) / numpy.array([width, height])
                SetCursorPos(int(cur_pos[0]//1), int(cur_pos[1]//1))

        frame = hands.draw_hand(frame, landmarks, hands.CONNECTION)
        if debug:
            cv2.imshow('Video', frame)

        if cv2.waitKey(40) == ord('q') & 0xFF:
            break
    except KeyboardInterrupt:
        print("\033[91mKeyboardInterrupt:  User interrupted the process.\033[0m")
        break
    except Exception as e:
        print(type(e).__name__, ":", e)
        break

video_capture.release()
cv2.destroyAllWindows()
print(f"\n{frame_count} Frames Processed !")
