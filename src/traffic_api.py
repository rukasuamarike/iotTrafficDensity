# traffic_api.py
from flask import Flask, jsonify
from traffic_stats import TrafficStats
from threading import Thread, Timer
import vehicletracker
import cv2

app = Flask(__name__)

# Initialize TrafficStats
traffic_stats = TrafficStats()

# Define a route to get traffic statistics
@app.route('/traffic-stats', methods=['GET'])
def get_traffic_stats():
    avg_5_min, avg_30_min, avg_1_hour, min_vehicles, max_vehicles, current_minute_count = traffic_stats.calculate_stats()
    return jsonify({
        'avg_5_min': avg_5_min,
        'avg_30_min': avg_30_min,
        'avg_1_hour': avg_1_hour,
        'min_vehicles': min_vehicles,
        'max_vehicles': max_vehicles,
        'current_minute_count': current_minute_count
    })

# Define a route to get raw vehicle logs
@app.route('/vehicle-logs', methods=['GET'])
def get_vehicle_logs():
    logs = list(traffic_stats.vehicle_log)
    return jsonify(logs)

# Define a route to get traffic trend
@app.route('/traffic-trend', methods=['GET'])
def get_traffic_trend():
    trend, is_rush_hour = traffic_stats.calculate_trend()
    return jsonify({
        'trend': trend,
        'is_rush_hour': is_rush_hour
    })

# Define a route to get 5-minute averages for the last hour
@app.route('/data-points', methods=['GET'])
def get_data_points():
    return jsonify(list(traffic_stats.data_points))

###def generate_frames():
    while True:
        frame = vehicletracker.get_current_frame()
        if frame is None:
            continue
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#@app.route('/video_feed')
###def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to periodically update data points
def periodic_update():
    traffic_stats.update_data_points()
    Timer(90, periodic_update).start()

# Run the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Start the vehicle tracker
    vehicletracker.start_tracker(traffic_stats)
    
    # Start periodic update
    periodic_update()
