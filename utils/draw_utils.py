import cv2

def draw_text(frame, text, pos=(10, 30), color=(0, 255, 0)):
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
