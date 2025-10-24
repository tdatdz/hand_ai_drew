import cv2
import mediapipe as mp
import numpy as np
from collections import deque
from gestures.gesture_rules import is_thumbs_up, is_ok_sign

# Config
INDEX_TIP_ID = 8
MAX_TRACE = 256

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# State
pts = deque(maxlen=MAX_TRACE)
last_label = ""

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam. Make sure camera is available and not used by other apps.")

print("Running. Press Q to quit, C to clear drawing.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    label = None

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        # Convert to numpy array (21,3)
        lm = np.array([[p.x * w, p.y * h, p.z * w] for p in hand.landmark])

        # Index fingertip
        index_tip = tuple(lm[INDEX_TIP_ID][:2].astype(int))
        pts.appendleft(index_tip)

        # Draw trail
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(MAX_TRACE / float(i + 1)) * 2)
            cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)

        # Gesture detection (rule-based)
        try:
            if is_thumbs_up(lm):
                label = "THUMBS UP 👍"
            elif is_ok_sign(lm):
                label = "OK 👌"
        except Exception:
            label = None

    # display label (keep last seen if none currently)
    if label:
        last_label = label
    cv2.putText(frame, last_label, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("AI Hand Drawing", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        pts.clear()

cap.release()
cv2.destroyAllWindows()
