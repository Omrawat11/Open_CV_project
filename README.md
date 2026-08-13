# 👁️ Open_CV_project

A collection of computer vision experiments built with **OpenCV**, **MediaPipe**, and **NumPy** — ranging from classic image processing filters to real-time pose/hand tracking with creative particle visualizations.

---

## 📂 Project Structure

```text
Open_CV_project/
├── data.py                    # Standalone edge detection script (Canny + Gaussian blur)
└── galaxy_pose/
    ├── galaxy_pose.py         # Real-time body-to-galaxy particle visualization
    ├── pos_Detect.py          # 3D two-hand skeleton tracker with fingertip bridges
    ├── test_mp.py             # MediaPipe pose gesture detection test script
    ├── pose_landmarker_lite.task
    ├── pose_landmarker.task
    ├── hand_landmarker.task
    └── README.md              # Detailed docs for the galaxy_pose sub-project
```

---

## 🧩 What's Inside

### 1. Edge Detection (`data.py`)
A simple OpenCV script that loads an image, converts it to grayscale, applies Gaussian blur to reduce noise, and runs Canny edge detection to visualize edges.

```bash
python data.py
```
> Note: update the `img_path` variable in the script to point to your own image before running.

### 2. Galaxy Pose (`galaxy_pose/`)
The core project — real-time webcam-based body pose tracking that turns your body into an animated galaxy of particles, with a spring-physics star cloud that can condense around your body or scatter explosively.

### 3. 3D Hand Tracker (`galaxy_pose/pos_Detect.py`)
Tracks both hands in real time using MediaPipe's Hand Landmarker, drawing depth-aware 3D skeletons and glowing fingertip-to-fingertip "bridges" between the two hands.

See [`galaxy_pose/README.md`](galaxy_pose/README.md) for full details, controls, and setup instructions for these scripts.

---

## 🛠️ Tech Stack

- **OpenCV** — image processing, video capture, rendering
- **MediaPipe** — real-time pose & hand landmark detection
- **NumPy** — numerical operations for particle physics

---

## 🚀 Quick Start

```bash
pip install opencv-python numpy mediapipe
python galaxy_pose/galaxy_pose.py
```

---

## 🔗 Repository Information

- **GitHub**: [Omrawat11/Open_CV_project](https://github.com/Omrawat11/Open_CV_project)
- **Author**: [Omrawat11](https://github.com/Omrawat11)
