import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8n_ncnn_model")

cap = cv2.VideoCapture(0)
# Loop through the video frames
while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting...")
        break

    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow("YOLOv8 Tracking", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
