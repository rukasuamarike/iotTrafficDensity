"""
# traffic_api.py
# Runs the Flask API server and starts the vehicle tracker in a separate thread.
# Owen Matejka
# CSEN 143
# Last Updated: 6/10/2024
"""

# Imports
from flask import Flask, jsonify
from traffic_stats import TrafficStats
from threading import Thread, Timer
import vehicletracker

app = Flask(__name__)

# Initialize TrafficStats
traffic_stats = TrafficStats()

# Route to get traffic statistics
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

# Route to get raw vehicle logs
@app.route('/vehicle-logs', methods=['GET'])
def get_vehicle_logs():
    logs = list(traffic_stats.vehicle_log)
    return jsonify(logs)

# Route to get traffic trend
@app.route('/traffic-trend', methods=['GET'])
def get_traffic_trend():
    trend, is_rush_hour = traffic_stats.calculate_trend()
    return jsonify({
        'trend': trend,
        'is_rush_hour': is_rush_hour
    })

# Route to get 5-minute averages for the last hour
@app.route('/data-points', methods=['GET'])
def get_data_points():
    return jsonify(list(traffic_stats.data_points))

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
