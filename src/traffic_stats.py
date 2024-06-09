from collections import deque
from datetime import datetime, timedelta

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
        minute_count = 0

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
        
        counts_5_min = [count[1] for count in self.per_minute_counts if count[0] >= last_5_min]
        counts_30_min = [count[1] for count in self.per_minute_counts if count[0] >= last_30_min]
        counts_1_hour = [count[1] for count in self.per_minute_counts if count[0] >= last_1_hour]
        
        avg_5_min = sum(counts_5_min) / len(counts_5_min) if counts_5_min else 0
        avg_30_min = sum(counts_30_min) / len(counts_30_min) if counts_30_min else 0
        avg_1_hour = sum(counts_1_hour) / len(counts_1_hour) if counts_1_hour else 0
        
        min_vehicles = min(counts_1_hour) if counts_1_hour else 0
        max_vehicles = max(counts_1_hour) if counts_1_hour else 0
        
        return avg_5_min, avg_30_min, avg_1_hour, min_vehicles, max_vehicles
