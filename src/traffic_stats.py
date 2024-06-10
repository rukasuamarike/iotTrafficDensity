from collections import deque
from datetime import datetime, timedelta
import numpy as np

class TrafficStats:
    def __init__(self):
        self.vehicle_log = deque()
        self.per_minute_counts = []

    def add_vehicle(self, vehicle_type):
        current_time = datetime.now()
        self.vehicle_log.append((current_time, vehicle_type))
        self._update_minute_counts()

    def _update_minute_counts(self):
        current_time = datetime.now()
        one_minute_ago = current_time - timedelta(minutes=1)

        while self.vehicle_log and self.vehicle_log[0][0] < one_minute_ago:
            self.vehicle_log.popleft()
        
        minute_count = len(self.vehicle_log)
        self.per_minute_counts.append((current_time, minute_count))

        # Keep only last 60 minutes of data
        one_hour_ago = current_time - timedelta(hours=1)
        self.per_minute_counts = [count for count in self.per_minute_counts if count[0] >= one_hour_ago]

    def calculate_stats(self):
        current_time = datetime.now()

        last_5_min = current_time - timedelta(minutes=5)
        last_30_min = current_time - timedelta(minutes=30)
        last_1_hour = current_time - timedelta(hours=1)
        one_minute_ago = current_time - timedelta(minutes=1)

        counts_5_min = [count[1] for count in self.per_minute_counts if count[0] >= last_5_min]
        counts_30_min = [count[1] for count in self.per_minute_counts if count[0] >= last_30_min]
        counts_1_hour = [count[1] for count in self.per_minute_counts if count[0] >= last_1_hour]
        counts_1_min = len([entry for entry in self.vehicle_log if entry[0] >= one_minute_ago])

        avg_5_min = sum(counts_5_min) / len(counts_5_min) if counts_5_min else 0
        avg_30_min = sum(counts_30_min) / len(counts_30_min) if counts_30_min else 0
        avg_1_hour = sum(counts_1_hour) / len(counts_1_hour) if counts_1_hour else 0

        min_vehicles = min(counts_1_hour) if counts_1_hour else 0
        max_vehicles = max(counts_1_hour) if counts_1_hour else 0

        return avg_5_min, avg_30_min, avg_1_hour, min_vehicles, max_vehicles, counts_1_min
    
    def calculate_trend(self):
        # Calculate trend based on the last 30 minutes of data
        current_time = datetime.now()
        thirty_minutes_ago = current_time - timedelta(minutes=30)
        recent_counts = [count[1] for time, count in self.per_minute_counts if time > thirty_minutes_ago]
        
        is_rush_hour = self.is_rush_hour(current_time)

        if len(recent_counts) < 5:
            return 'calculating', is_rush_hour  # Not enough data to determine trend
        
        # Exponential smoothing to give more weight to recent data
        alpha = 0.3  # Smoothing factor, can be adjusted
        smoothed_counts = [recent_counts[0]]  # Initialize with the first count

        for count in recent_counts[1:]:
            smoothed_counts.append(alpha * count + (1 - alpha) * smoothed_counts[-1])

        differences = np.diff(smoothed_counts)
        avg_difference = np.mean(differences)
        std_dev = np.std(differences)

        if is_rush_hour(current_time):
            threshold_increase = std_dev * 1.5
            threshold_decrease = -std_dev * 1.5
        else:
            threshold_increase = std_dev
            threshold_decrease = -std_dev

        # Use standard deviation to determine significant changes
        if avg_difference > threshold_increase:
            return 'increasing', is_rush_hour
        elif avg_difference < threshold_decrease:
            return 'decreasing', is_rush_hour
        else:
            return 'stable', is_rush_hour
        
    # Additional method to identify rush hours
    def is_rush_hour(self, current_time=None):
        if current_time is None:
            current_time = datetime.now()
        hour = current_time.hour
        # Define rush hours (e.g., 7-9:30 AM and 3:00-5:30 PM)
        return (7 <= hour <= 9.5) or (15 <= hour <= 17.5)
    