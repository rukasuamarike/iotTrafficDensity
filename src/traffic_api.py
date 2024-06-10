from flask import Flask, jsonify
from traffic_stats import TrafficStats
from threading import Thread
import vehicletracker

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

# Run the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Start the vehicle tracker
    vehicletracker.start_tracker(traffic_stats)
