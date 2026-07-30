import cv2
import numpy as np 

img_path = r"C:\Users\TUF\Desktop\all photos\WhatsApp Image 2026-05-02 at 11.07.51.jpeg"
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"Could not open or read image at path: {img_path}")

# convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# blur t0 reduce noise
blured = cv2.GaussianBlur(gray, (5, 5), 0)

#detect edges with canny
edges = cv2.Canny(blured, 50, 150, apertureSize=3)

#Threshold 1=50, Threshold 2=150
cv2.imshow('Edges', edges)
cv2.waitKey(0)

