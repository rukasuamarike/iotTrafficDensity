import cv2
from ultralytics import YOLO
import time
import numpy as np

# COCO vehicle class IDs
VEHICLE_CLASS_IDS = [2, 3, 5, 7]  # Car, Motorcycle, Bus, Truck

# ROI for tracking (only consider vehicles touching both lines)
roi_line_y_top = 175
roi_line_y_bottom = 185

# Calculate the center of a bounding box
def get_center(bbox):
    x1, y1, x2, y2 = bbox
    return (int((x1 + x2) / 2), int((y1 + y2) / 2))

# Calculate the direction of movement
def get_direction(center, previous_center):
    if previous_center:
        if center[0] > previous_center[0]:
            return "right"
        elif center[0] < previous_center[0]:
            return "left"
    return "stationary"

# Map class IDs to vehicle types
class_id_to_vehicle_type = {
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck'
}

def start_tracker(traffic_stats):
    # Load the model
    model = YOLO("yolov8s_full_integer_quant_edgetpu.tflite")

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    # Set frame width/height
    frame_width = 640
    frame_height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Dictionary for storing tracked vehicle information
    tracked_vehicles = {}
    vehicle_counter = {'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0}

    # Loop through the video frames
    while True:
        start_time = time.time()
        
        # Read frame from the video
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame! Exiting....")
            break

        # Run tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, imgsz=480)

        # Filter results to only keep vehicles
        vehicle_detections = [d for d in results[0].boxes if int(d.cls) in VEHICLE_CLASS_IDS]

        # Visualize the vehicle detections on the frame and update tracking info
        for det in vehicle_detections:
            bbox = det.xyxy[0].cpu().numpy()  # Bounding box coordinates
            conf = det.conf[0]  # Confidence score
            cls = int(det.cls[0])    # Class ID
            x1, y1, x2, y2 = map(int, bbox)
            vehicle_type = class_id_to_vehicle_type[cls]

            track_id = int(det.id[0]) if det.id is not None else None
            
            # Consider only vehicles touching both the top and bottom ROI lines
            if track_id is not None and y1 < roi_line_y_bottom and y2 > roi_line_y_top and y2 >= roi_line_y_bottom and y1 <= roi_line_y_top:
                center = get_center(bbox)
                if track_id in tracked_vehicles:
                    previous_center = tracked_vehicles[track_id]['center']
                    direction = get_direction(center, previous_center)
                    if direction == "right" and tracked_vehicles[track_id]['counted'] == False:
                        vehicle_counter[vehicle_type] += 1
                        tracked_vehicles[track_id]['counted'] = True
                        traffic_stats.add_vehicle(vehicle_type)
                    tracked_vehicles[track_id]['center'] = center
                    tracked_vehicles[track_id]['direction'] = direction
                else:
                    tracked_vehicles[track_id] = {'center': center, 'direction': 'stationary', 'counted': False}
            
                # Draw bounding box and label on the frame
                label = f"{vehicle_type.capitalize()}: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the vehicle counters
        counter_text = f"Cars: {vehicle_counter['car']} Motorcycles: {vehicle_counter['motorcycle']} Buses: {vehicle_counter['bus']} Trucks: {vehicle_counter['truck']}"
        cv2.putText(frame, counter_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display traffic density statistics
        avg_5_min, avg_30_min, avg_1_hour, min_vehicles, max_vehicles, current_minute_count = traffic_stats.calculate_stats()
        stats_text = f"5 min avg: {avg_5_min:.2f} 30 min avg: {avg_30_min:.2f} 1 hour avg: {avg_1_hour:.2f} Min: {min_vehicles} Max: {max_vehicles} Current Min: {current_minute_count}"
        cv2.putText(frame, stats_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        # Draw the ROI lines
        cv2.line(frame, (0, roi_line_y_top), (frame_width, roi_line_y_top), (255, 0, 0), 2)
        cv2.line(frame, (0, roi_line_y_bottom), (frame_width, roi_line_y_bottom), (255, 0, 0), 2)
        
        # Display the annotated frame
        cv2.imshow("Matejka-Amlicke Vehicle Tracker", frame)

        # Calculate the processing time and delay to limit frame rate
        end_time = time.time()
        elapsed_time = end_time - start_time
        delay = max(1, int((1 / 10) - elapsed_time * 1000))  # Aiming for 10 FPS
        if cv2.waitKey(delay) & 0xFF == ord("q"):
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
