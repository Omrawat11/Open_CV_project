# 🌌 Galaxy Pose - Interactive Body Particle Visualization

An interactive real-time computer vision project built using **OpenCV**, **MediaPipe**, and **NumPy**. It captures pose landmarks from a webcam feed and transforms the user's body into a dynamic galaxy particle cloud with smooth spring physics, flickering stars, and scatter/condense visual effects.

---

## 📸 Overview & Features

- **Real-Time Body Pose Tracking**: Uses MediaPipe Pose Landmarker to track 33 3D body keypoints in real time.
- **Dynamic Star Cloud Physics**: Renders hundreds of animated stars along body limbs with customized spring velocity, damping, and flicker animations.
- **Interactive Controls**: Toggle between **CONDENSED** (body-aligned galaxy) and **SCATTER** (explosive particle dispersion with fading ghost stars).
- **Dark Space Aesthetics**: Blends the webcam video with a deep space particle overlay for a futuristic visual experience.

---

## 🛠️ Project Structure

```text
galaxy_pose/
├── galaxy_pose.py             # Main entry point for Galaxy Pose visualization
├── pos_Detect.py              # Hand 3D landmark & skeleton tracking module
├── test_mp.py                 # MediaPipe pose gesture detection test script
├── data.py                    # OpenCV edge detection filter script
├── pose_landmarker_lite.task  # MediaPipe Pose Landmarker model asset
├── pose_landmarker.task       # MediaPipe Full Pose model asset
├── hand_landmarker.task       # MediaPipe Hand Landmarker model asset
└── README.md                  # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites & Dependencies

Ensure you have Python 3.9 or higher installed. Install the required Python packages:

```bash
pip install opencv-python numpy mediapipe
```

### 2. Running Galaxy Pose

Run the main application script:

```bash
python galaxy_pose/galaxy_pose.py
```

### 3. Controls

| Key | Action |
| --- | --- |
| `SPACE` | Toggle between **Condensed** galaxy body and **Scatter** particle explosion |
| `Q` | Quit application |

---

## 🔗 Repository Information

- **GitHub Repository**: [https://github.com/Omrawat11/Open_CV_project](https://github.com/Omrawat11/Open_CV_project)
- **Author**: Omrawat11
