import gestures


gestures_ = {
    gestures.gesture1: "Pointing Upwards",
}


def detect_gesture(landmarks) -> str:
    for func, name in gestures_.items():
        if func(landmarks):
            return name
    return "Unknown Gesture"
