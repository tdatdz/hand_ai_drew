import numpy as np

THUMB_TIP_ID = 4
INDEX_TIP_ID = 8
WRIST_ID = 0

def dist(a, b):
    return np.linalg.norm(a - b)

def is_thumbs_up(lm):
    """Simple heuristic for thumbs-up:
    - Thumb tip is higher (smaller y) than wrist by some margin
    - Other fingertips (index/middle/ring/pinky) are near the palm (folded)
    """
    try:
        thumb_tip = lm[THUMB_TIP_ID][:2]
        wrist = lm[WRIST_ID][:2]
        tips = [lm[8][:2], lm[12][:2], lm[16][:2], lm[20][:2]]
    except Exception:
        return False

    # image coords: y increases downward; check thumb above wrist by threshold
    if thumb_tip[1] > wrist[1] - 30:
        return False

    # folded if fingertip close to wrist
    folded = sum(1 for t in tips if dist(t, wrist) < 80)
    return folded >= 3

def is_ok_sign(lm):
    """Heuristic for OK: thumb tip and index tip are close (forming a circle)."""
    try:
        thumb = lm[THUMB_TIP_ID][:2]
        index = lm[INDEX_TIP_ID][:2]
        scale = dist(lm[WRIST_ID][:2], lm[9][:2]) + 1e-6
    except Exception:
        return False
    d = dist(thumb, index)
    return d < 0.35 * scale
