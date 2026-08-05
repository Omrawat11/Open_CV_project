import os
import cv2
import math
import random
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import PoseLandmarksConnections

# ================= SETTINGS =================
MAX_BODY_STARS = 1200
GHOST_LIMIT = 3000
GHOST_PER_STAR = 1

# Helper to locate model asset file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = 'pose_landmarker_lite.task'
MODEL_PATH = os.path.join(SCRIPT_DIR, MODEL_NAME)

if not os.path.exists(MODEL_PATH):
    # Fallback to parent workspace folder if run from parent directory
    PARENT_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), MODEL_NAME)
    if os.path.exists(PARENT_PATH):
        MODEL_PATH = PARENT_PATH
    else:
        MODEL_PATH = MODEL_NAME  # Fallback to current working directory

# ================= BODY STAR =================
class BodyStar:
    def __init__(self, tx, ty):
        self.tx = float(tx)
        self.ty = float(ty)

        self.x = tx + random.uniform(-20, 20)
        self.y = ty + random.uniform(-20, 20)

        self.vx = 0
        self.vy = 0

        self.phase = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.05, 0.15)

        self.size = random.choice([1, 2])

    def scatter(self):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(10, 40)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(self, condensed, frame_idx):
        k = 0.22 if condensed else 0.04
        d = 0.60 if condensed else 0.90

        self.vx += (self.tx - self.x) * k
        self.vy += (self.ty - self.y) * k

        self.vx *= d
        self.vy *= d

        self.x += self.vx
        self.y += self.vy

        self.flicker = 0.5 + 0.5 * abs(
            math.sin(frame_idx * self.speed + self.phase)
        )

    def draw(self, canvas):
        x = int(self.x)
        y = int(self.y)

        h, w = canvas.shape[:2]

        if 0 <= x < w and 0 <= y < h:
            brightness = int(255 * self.flicker)

            cv2.circle(
                canvas,
                (x, y),
                self.size,
                (brightness, brightness, brightness),
                -1
            )

# ================= GHOST STAR =================
class GhostStar:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(5, 20)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.alpha = 1.0
        self.fade = random.uniform(0.01, 0.03)

        self.size = random.choice([1, 2])

    @property
    def alive(self):
        return self.alpha > 0

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.96
        self.vy *= 0.96

        self.alpha -= self.fade

    def draw(self, canvas):
        if self.alpha <= 0:
            return

        x = int(self.x)
        y = int(self.y)

        h, w = canvas.shape[:2]

        if 0 <= x < w and 0 <= y < h:
            brightness = int(255 * self.alpha)

            cv2.circle(
                canvas,
                (x, y),
                self.size,
                (brightness, brightness, brightness),
                -1
            )

# ================= GENERATE BODY POINTS =================
def generate_body_points(landmarks, width, height):
    points = []

    connections = PoseLandmarksConnections.POSE_LANDMARKS

    for connection in connections:
        start_idx = connection.start
        end_idx = connection.end

        start = landmarks[start_idx]
        end = landmarks[end_idx]

        x1 = int(start.x * width)
        y1 = int(start.y * height)

        x2 = int(end.x * width)
        y2 = int(end.y * height)

        dist = int(math.hypot(x2 - x1, y2 - y1))

        for i in range(0, dist, 8):
            t = i / max(dist, 1)

            px = int(x1 + (x2 - x1) * t)
            py = int(y1 + (y2 - y1) * t)

            points.append((px, py))

    # Add extra body volume
    extra = []

    for px, py in points:
        for _ in range(2):
            extra.append((
                px + random.randint(-15, 15),
                py + random.randint(-15, 15)
            ))

    points.extend(extra)

    # Limit points
    if len(points) > MAX_BODY_STARS:
        points = random.sample(points, MAX_BODY_STARS)

    return points

# ================= MAIN =================
def main():

    print("\n* Full Body Galaxy Cloud *")
    print(f"Using model asset: {MODEL_PATH}")
    print("Press SPACE -> Scatter/Condense")
    print("Press Q -> Quit\n")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Webcam not found")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
    )
    detector = vision.PoseLandmarker.create_from_options(options)

    body_stars = []
    ghost_stars = []

    condensed = False
    prev_condensed = False

    frame_idx = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        results = detector.detect(mp_image)

        landmarks = None

        if results and results.pose_landmarks:
            landmarks = results.pose_landmarks[0]

        # ===== KEYBOARD =====
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            condensed = not condensed

        elif key == ord('q'):
            break

        # ===== BODY POINTS =====
        if landmarks and frame_idx % 3 == 0:

            points = generate_body_points(landmarks, w, h)

            if not body_stars:
                for px, py in points:
                    body_stars.append(BodyStar(px, py))

            else:

                while len(body_stars) < len(points):
                    px, py = points[len(body_stars)]
                    body_stars.append(BodyStar(px, py))

                body_stars = body_stars[:len(points)]

                random.shuffle(points)

                for i, (px, py) in enumerate(points):
                    body_stars[i].tx = px
                    body_stars[i].ty = py

        # ===== SCATTER EFFECT =====
        if prev_condensed and not condensed:

            for star in body_stars:
                star.scatter()

            subset = random.sample(
                body_stars,
                min(len(body_stars), 400)
            )

            for star in subset:
                for _ in range(GHOST_PER_STAR):
                    ghost_stars.append(
                        GhostStar(star.x, star.y)
                    )

        prev_condensed = condensed

        # ===== CLEAN GHOSTS =====
        ghost_stars = [g for g in ghost_stars if g.alive]

        if len(ghost_stars) > GHOST_LIMIT:
            ghost_stars = ghost_stars[-GHOST_LIMIT:]

        # ===== DRAW =====
        dark_bg = (frame * 0.25).astype(np.uint8)

        star_layer = np.zeros_like(frame)

        # Draw ghosts
        for ghost in ghost_stars:
            ghost.update()
            ghost.draw(star_layer)

        # Draw body stars
        for star in body_stars:
            star.update(condensed, frame_idx)
            star.draw(star_layer)

        # Combine
        output = cv2.add(dark_bg, star_layer)

        # HUD
        mode = "CONDENSED" if condensed else "SCATTER"

        cv2.putText(
            output,
            f"MODE: {mode}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output,
            f"Stars: {len(body_stars)}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            1
        )

        cv2.putText(
            output,
            "SPACE = toggle  |  Q = quit",
            (20, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1
        )

        cv2.imshow("* Galaxy Body Cloud *", output)

        frame_idx += 1

    detector.close()
    cap.release()
    cv2.destroyAllWindows()

# ================= RUN =================
if __name__ == "__main__":
    main()
