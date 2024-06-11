# CSEN 143 Traffic Density System

This project calculates the Northbound traffic density on Lafayette Street in Santa Clara using YOLOv8, a Raspberry Pi 5, and a Google Coral TPU. Developed for the CSEN 143 (Internet of Things) course, it provides real-time traffic analysis and visualization.

<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/rukasuamarike/iotTrafficDensity/assets/69021860/db05a287-db27-42b2-af0f-06f612b8a8a3" alt="website_view" style="width: 55%;">
    <img src="https://github.com/rukasuamarike/iotTrafficDensity/assets/69021860/2a3f0494-a8a9-4c98-98ac-76c61ab3fdcc" alt="image_detection" style="width: 43%;">
</div>


## Contributors
- Owen Matejka
- Lucas Amlicke

## Project Overview

The Traffic Density System utilizes advanced object detection to monitor vehicle flow. The system quantifies traffic congestion levels using YOLOv8, offering valuable data for urban planning and traffic management. Our goal is to demonstrate that reliable computer vision algorithms targeting transportation planning can be deployed at the edge on inexpensive devices.

## Requirements
- Raspberry Pi 5 running Raspberry Pi OS 12 (Bookworm)
- Google Coral TPU
- USB Camera

## Installation Guide

Follow these steps to set up and run the Traffic Density System:

1. **Clone the Repository**
   - Use `git clone https://github.com/rukasuamarike/iotTrafficDensity` to download the project files.
2. **Set Up Python Environment**
   - Ensure Python 3.9.0 is installed.
   - Create and activate a virtual environment.
     ```
     python3 -m venv env
     source env/bin/activate
     ```
3. **Install Dependencies**
   - Install required Python packages which can be viewed under Github insights.
     
4. **Install Coral Runtime**
   - Download and install the Coral runtime from [Coral runtime](https://github.com/feranick/libedgetpu/releases).
5. **Camera Setup**
   - Position a USB camera to face Lafayette Street from a perpendicular angle and connect it to the Raspberry Pi.
6. **Start the System**
   - Execute `python traffic_api.py` to initiate the traffic analysis.
7. **Adjust ROI Lines**
   - Modify ROI lines in `vehicletracker.py` as necessary to accurately track vehicles.
8. **Webserver Configuration (Optional)**
   - Update `website/config.js` with the URL that the Flask server is deployed to
   - Visit the page to view the data!

## Viewing Camera Feed Remotely

For remote camera feed access, utilize RPi-Connect (https://www.raspberrypi.com/software/connect/). This tool enables an efficient remote desktop experience, allowing you to monitor the OpenCV video feed from anywhere.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

## Support

For support, please open an issue in the GitHub repository.