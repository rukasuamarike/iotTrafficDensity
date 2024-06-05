import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Detects phones
WATER_BOTTLE_CLASS_ID = 67

# Initialize camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Process frame with YOLO
    results = model(frame)

    # Draw results on the frame
    for result in results:
        for bbox in result.boxes:
            cls = int(bbox.cls[0])
            if cls == WATER_BOTTLE_CLASS_ID:
                # Extract bounding box coordinates
                x1, y1, x2, y2 = map(int, bbox.xyxy[0])
                conf = float(bbox.conf[0])
                label = f'Cell Phone: {conf:.2f}'
                
                # Draw rectangle and label on frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('YOLO Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
