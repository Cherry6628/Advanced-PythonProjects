import cv2
import numpy
from mediapipe import solutions


white = (0xFF, 0xFF, 0xFF)
red = (0x00, 0x00, 0xFF)
blue = (0xFF, 0x00, 0x00)
green = (0x00, 0xFF, 0x00)
yellow = (0x00, 0xFF, 0xFF)
pink = (0xFF, 0x00, 0xFF)
black = (0x00, 0x00, 0x00)

CONNECTION = frozenset({
    (0, 1, white),
    (0, 5, white),
    (5, 9, white),
    (9, 13, white),
    (13, 17, white),
    (0, 17, white),

    (1, 2, red),
    (2, 3, red),
    (3, 4, red),

    (5, 6, blue),
    (6, 7, blue),
    (7, 8, blue),

    (9, 10, green),
    (10, 11, green),
    (11, 12, green),

    (13, 14, yellow),
    (14, 15, yellow),
    (15, 16, yellow),

    (17, 18, pink),
    (18, 19, pink),
    (19, 20, pink),

    # additional
    # (0, 9, black),
    # (0, 13, black),
    # (1, 5, black)
})

model = solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.89)
del solutions


def detect_hands(image):
    h, w, _ = image.shape
    hands_ = (model.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))).multi_hand_landmarks

    all_h = []
    if not hands_:
        return numpy.array(all_h)
    for hand in hands_:
        h1 = []
        for point in hand.landmark:
            x, y, z = int(point.x * w), int(point.y * h), point.z
            h1.append((x, y, z))
        all_h.append(h1)
    return numpy.array(all_h)


def draw_hand(frame, points, connections):
    for hand in points:
        for x in connections:
            p1 = hand[x[0]]
            p2 = hand[x[1]]
            x1, y1 = int(p1[0]), int(p1[1])
            x2, y2 = int(p2[0]), int(p2[1])
            c = (0xFF, 0xFF, 0xFF)
            if len(x) > 2:
                c = x[2]
            if len(x) > 3:
                raise Exception(
                    f"Got {len(x)} values in each connection data; Expected 2 to 3 values per connection.\n[(point_index_i, point_index_j, optional_color), ...] is the Expected Structure.")
            cv2.line(frame, (x1, y1), (x2, y2), c, 2)
        for x, y, _ in hand:
            f = lambda e: min(int((abs(_)**(1/2))*255*2), 255)
            c = (f(_), f(_), f(_))
            cv2.circle(frame, (int(x), int(y)), 2, c, 2)
    return frame
