import cv2
from ultralytics import YOLO
import time

# Load the YOLOv8 model
model = YOLO("yolov8n_ncnn_model")

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set the desired frame width and height
frame_width = 320
frame_height = 240
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Define the class ID for phones
PHONE_CLASS_ID = 67

# Loop through the video frames
while True:
    # Capture start time
    start_time = time.time()
    
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting...")
        break

    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True)

    # Filter results to only keep phones
    phone_detections = [d for d in results[0].boxes if int(d.cls) == PHONE_CLASS_ID]

    # Visualize the phone detections on the frame
    for det in phone_detections:
        bbox = det.xyxy[0].cpu().numpy()  # Bounding box coordinates
        conf = det.conf[0]  # Confidence score
        cls = int(det.cls[0])    # Class ID
        
        # Draw bounding box and label on the frame
        x1, y1, x2, y2 = map(int, bbox)
        label = f"Phone: {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the annotated frame
    cv2.imshow("YOLOv8 Tracking", frame)

    # Calculate the processing time and delay to limit frame rate
    end_time = time.time()
    elapsed_time = end_time - start_time
    delay = max(1, int((1 / 10) - elapsed_time * 1000))  # Aiming for 10 FPS
    if cv2.waitKey(delay) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
