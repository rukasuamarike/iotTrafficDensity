# traffic_stats.py
from datetime import datetime, timedelta
from collections import deque
import math

class Vehicle:
    def __init__(self, time_detected, vehicle_type):
        self.time_detected = time_detected
        self.vehicle_type = vehicle_type

class TrafficStats:
    def __init__(self):
        self.vehicle_deque = deque()
        self.vehicle_log = deque(maxlen=100)
        self.total_vehicles_added = 0
        self.start_time = datetime.now()
        self.vehicles_in_current_minute = 0
        self.current_minute_window_start = self.start_time

    def add_vehicle(self, vehicle_type):
        self.update()  # Ensure we call update to handle minute changes
        current_time = datetime.now()
        vehicle = Vehicle(current_time, vehicle_type)
        self.vehicle_deque.append(vehicle)
        self.vehicle_log.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), vehicle_type))  # Log the vehicle
        self.total_vehicles_added += 1
        
        self.vehicles_in_current_minute += 1
        print(f"Vehicle added: {vehicle_type} at {current_time.strftime('%H:%M:%S')}. Total vehicles added so far: {self.total_vehicles_added}. Vehicles added in the current minute: {self.vehicles_in_current_minute}")

    def update(self):
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)
        while self.vehicle_deque and self.vehicle_deque[0].time_detected < one_hour_ago:
            self.vehicle_deque.popleft()

        # Calculate current window based on start time
        elapsed_time = (current_time - self.start_time).total_seconds()
        new_minute_window_start = self.start_time + timedelta(minutes=int(elapsed_time // 60))
        
        # Reset the counter if we are in a new minute window
        if new_minute_window_start > self.current_minute_window_start:
            self.vehicles_in_current_minute = 0
            self.current_minute_window_start = new_minute_window_start

        print(f"Update at {current_time.strftime('%H:%M:%S')}. Vehicles in deque: {len(self.vehicle_deque)}. Current minute window: {self.current_minute_window_start.strftime('%H:%M:%S')} to {(self.current_minute_window_start + timedelta(minutes=1)).strftime('%H:%M:%S')}")

    def count_vehicles_in_window(self, start_time, end_time):
        return sum(1 for vehicle in self.vehicle_deque if start_time <= vehicle.time_detected < end_time)

    def average_vehicles_over_period(self, minutes):
        current_time = datetime.now()
        # Round up to the next minute
        next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
        
        # Calculate the start time for each of the last `minutes` minute windows
        total_minutes = math.ceil((current_time - self.start_time).total_seconds() / 60)
        if total_minutes < minutes:
            minutes = total_minutes  # Adjust if we have less data than the requested period
        
        intervals = [(next_minute - timedelta(minutes=i+1), next_minute - timedelta(minutes=i)) for i in range(minutes)]

        vehicle_counts = [self.count_vehicles_in_window(start, end) for start, end in intervals]
        
        valid_intervals = len([count for count in vehicle_counts if count > 0])
        valid_intervals = valid_intervals if valid_intervals > 0 else 1  # To avoid division by zero
        
        return sum(vehicle_counts) / valid_intervals

    def min_max_vehicles_last_hour(self):
        current_time = datetime.now()
        next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
        one_hour_ago = current_time - timedelta(hours=1)
        
        total_minutes = math.ceil((current_time - self.start_time).total_seconds() / 60)
        minutes = min(total_minutes, 60)  # Adjust to the last hour or the available data
        
        intervals = [(next_minute - timedelta(minutes=i+1), next_minute - timedelta(minutes=i)) for i in range(minutes)]
        
        vehicle_counts = [self.count_vehicles_in_window(start, end) for start, end in intervals]
        
        if not vehicle_counts:
            return 0, 0  # No data available
        
        min_vehicles = min(vehicle_counts)
        max_vehicles = max(vehicle_counts)
        
        return min_vehicles, max_vehicles

    def determine_trend(self):
        current_time = datetime.now()
        total_minutes = math.ceil((current_time - self.start_time).total_seconds() / 60)
        if total_minutes < 5:
            return 'calculating'
        
        # Calculate the vehicle counts for the last 5 minutes
        next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
        intervals = [(next_minute - timedelta(minutes=i+1), next_minute - timedelta(minutes=i)) for i in range(5)]
        vehicle_counts = [self.count_vehicles_in_window(start, end) for start, end in intervals]
        
        # Determine the trend based on the changes in vehicle counts
        increasing = all(x < y for x, y in zip(vehicle_counts, vehicle_counts[1:]))
        decreasing = all(x > y for x, y in zip(vehicle_counts, vehicle_counts[1:]))
        
        if increasing:
            return 'increasing'
        elif decreasing:
            return 'decreasing'
        else:
            return 'stable'

    def calculate_stats(self):
        avg_5_min = self.average_vehicles_over_period(5)
        avg_30_min = self.average_vehicles_over_period(30)
        avg_1_hour = self.average_vehicles_over_period(60)
        min_vehicles, max_vehicles = self.min_max_vehicles_last_hour()
        current_minute_start = datetime.now() - timedelta(minutes=1)
        current_minute_count = self.count_vehicles_in_window(current_minute_start, datetime.now())
        return avg_5_min, avg_30_min, avg_1_hour, min_vehicles, max_vehicles, current_minute_count

    def calculate_trend(self):
        trend = self.determine_trend()
        
        current_time = datetime.now().time()
        morning_rush_start = datetime.strptime("07:00", "%H:%M").time()
        morning_rush_end = datetime.strptime("09:30", "%H:%M").time()
        evening_rush_start = datetime.strptime("15:00", "%H:%M").time()
        evening_rush_end = datetime.strptime("17:30", "%H:%M").time()

        if (morning_rush_start <= current_time <= morning_rush_end) or (evening_rush_start <= current_time <= evening_rush_end):
            is_rush_hour = True
        else:
            is_rush_hour = False

        return trend, is_rush_hour
