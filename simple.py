import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Load pretrain or fine-tune model
# Process the image
cap = cv2.VideoCapture(1)

# Define colors for bounding boxes and text
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting...")
        break
    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv8 Inference", annotated_frame)
    # Exit loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break
# Release resources
cap.release()
cv2.destroyAllWindows()