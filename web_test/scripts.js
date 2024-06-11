document.addEventListener("DOMContentLoaded", function() {
    // Load the server URL from config.js
    const apiStatsUrl = `${serverUrl}/traffic-stats`;
    const apiLogsUrl = `${serverUrl}/vehicle-logs`;
    const apiTrendUrl = `${serverUrl}/traffic-trend`;
    const apiDataPointsUrl = `${serverUrl}/data-points`;
    const videoFeedUrl = `${serverUrl}/video_feed`;

    // Set the src of the camera feed image
    document.getElementById('camera-feed').src = videoFeedUrl;

    const maxLogEntries = 50;
    let vehicleLogs = [];
    let logSet = new Set();

    const ctx = document.getElementById('trafficVolumeChart').getContext('2d');
    const trafficVolumeChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Traffic Volume',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Average Cars Per Minute (5-Min-AVG)'
                    },
                    suggestedMax: 10  // Default value which will be updated dynamically
                }
            }
        }
    });

    async function fetchTrafficStats() {
        try {
            const response = await fetch(apiStatsUrl, {
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420"
                })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Traffic Stats Data:", data); // Logging the data

            // Format the values to 2 decimal points
            const formatNumber = (num) => num !== null ? num.toFixed(2) : 'N/A';

            document.querySelector('.hourly-average').textContent = formatNumber(data.avg_1_hour);
            document.querySelector('.thirty-minute-average').textContent = formatNumber(data.avg_30_min);
            document.querySelector('.five-minute-average').textContent = formatNumber(data.avg_5_min);
            document.querySelector('.max-vehicles').textContent = data.max_vehicles;
            document.querySelector('.min-vehicles').textContent = data.min_vehicles;

            // Update current minute count
            const currentMinuteCount = data.current_minute_count || 0;
            document.querySelector('.current-minute-count').textContent = currentMinuteCount;

        } catch (error) {
            console.error('Error fetching traffic stats:', error);
            document.querySelector('.hourly-average').textContent = 'N/A';
            document.querySelector('.thirty-minute-average').textContent = 'N/A';
            document.querySelector('.five-minute-average').textContent = 'N/A';
            document.querySelector('.max-vehicles').textContent = 'N/A';
            document.querySelector('.min-vehicles').textContent = 'N/A';
            document.querySelector('.current-minute-count').textContent = 'N/A';
        }
    }

    async function fetchVehicleLogs() {
        try {
            const response = await fetch(apiLogsUrl, {
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420"
                })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Vehicle Logs Data:", data); // Logging the data

            // Update vehicleLogs array and logSet to avoid duplicates
            data.forEach(log => {
                const logEntry = JSON.stringify(log);
                if (!logSet.has(logEntry)) {
                    vehicleLogs.unshift(log); // Add new logs to the beginning
                    logSet.add(logEntry);
                }
            });

            if (vehicleLogs.length > maxLogEntries) {
                vehicleLogs = vehicleLogs.slice(0, maxLogEntries);
                logSet = new Set(vehicleLogs.map(log => JSON.stringify(log)));
            }

            // Update the table with the stored logs
            const logTableBody = document.querySelector('.vehicle-log tbody');
            logTableBody.innerHTML = ''; // Clear existing logs
            vehicleLogs.forEach(log => {
                const logRow = document.createElement('tr');
                logRow.classList.add('border-b', 'transition-colors', 'hover:bg-muted/50', 'data-[state=selected]:bg-muted');
                const timeCell = document.createElement('td');
                timeCell.classList.add('p-4', 'align-middle', '[&:has([role=checkbox])]:pr-0');
                timeCell.textContent = log[0];
                const typeCell = document.createElement('td');
                typeCell.classList.add('p-4', 'align-middle', '[&:has([role=checkbox])]:pr-0');
                typeCell.textContent = log[1];
                logRow.appendChild(timeCell);
                logRow.appendChild(typeCell);
                logTableBody.appendChild(logRow);
            });
        } catch (error) {
            console.error('Error fetching vehicle logs:', error);
            const logTableBody = document.querySelector('.vehicle-log tbody');
            logTableBody.innerHTML = '<tr><td colspan="2" class="p-4 text-center">N/A</td></tr>';
        }
    }

    async function fetchTrafficTrend() {
        try {
            const response = await fetch(apiTrendUrl, {
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420"
                })
            });
            const data = await response.json();
            console.log("Traffic Trend Data:", data); // Logging the data

            let trendText = '';
            let trendMessage = '';
            let rushHourMessage = '';
            let trendClass = 'bg-gray-500'; // Default to stable (grey)

            if (data.is_rush_hour) {
                rushHourMessage = `It is currently rush hour, which lasts from 7-9:30 AM and 3:00-5:30 PM.`;
            } else {
                rushHourMessage = `It is currently not rush hour.`;
            }

            if (data.trend === 'increasing') {
                trendText = `Increasing`;
                trendMessage = `The traffic level over the last 15 minutes is increasing. ` + rushHourMessage;
                trendClass = 'bg-red-500'; // Set class to red for increasing
            } else if (data.trend === 'decreasing') {
                trendText = `Decreasing`;
                trendMessage = `The traffic level over the last 15 minutes is decreasing. ` + rushHourMessage;
                trendClass = 'bg-green-500'; // Set class to green for decreasing
            } else if (data.trend === 'stable') {
                trendText = `Stable`;
                trendMessage = `The traffic level over the last 15 minutes has remained stable. ` + rushHourMessage;
            } else {
                trendText = `Calculating`;
                trendMessage = `The traffic level is being calculated.`;
                trendClass = 'bg-blue-500'; // Set class to blue while calculating
            }

            document.querySelector('.current-traffic-level-text').textContent = trendMessage;
            const trendElement = document.querySelector('.traffic-trend');
            trendElement.textContent = trendText;
            trendElement.className = `rounded-full px-3 py-1 text-sm font-medium text-white traffic-trend ${trendClass}`;

            // Update the Chart.js data
            trafficVolumeChart.data.labels.push(new Date());
            trafficVolumeChart.data.datasets[0].data.push(data.current_minute_count);
            trafficVolumeChart.update();

        } catch (error) {
            console.error('Error fetching traffic trend:', error);
            document.querySelector('.current-traffic-level-text').textContent = 'The current traffic level is N/A.';
            const trendElement = document.querySelector('.traffic-trend');
            trendElement.textContent = 'N/A';
            trendElement.className = `rounded-full px-3 py-1 text-sm font-medium text-white traffic-trend bg-gray-500`;
        }
    }

    async function fetchDataPoints() {
        try {
            const response = await fetch(apiDataPointsUrl, {
                headers: new Headers({
                    "ngrok-skip-browser-warning": "69420"
                })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Data Points:", data); // Logging the data

            // Clear existing data
            trafficVolumeChart.data.labels = [];
            trafficVolumeChart.data.datasets[0].data = [];

            let maxValue = 0;

            // Populate chart with new data
            data.forEach(point => {
                trafficVolumeChart.data.labels.push(new Date(point.timestamp));
                trafficVolumeChart.data.datasets[0].data.push(point.average);
                if (point.average > maxValue) {
                    maxValue = point.average;
                }
            });

            // Update the suggestedMax value
            trafficVolumeChart.options.scales.y.suggestedMax = maxValue + 5;

            trafficVolumeChart.update();

        } catch (error) {
            console.error('Error fetching data points:', error);
        }
    }

    // Initial fetch
    fetchTrafficStats();
    fetchVehicleLogs();
    fetchTrafficTrend();
    fetchDataPoints();

    // Re-fetch every minute
    setInterval(() => {
        fetchTrafficStats();
        fetchVehicleLogs();
        fetchTrafficTrend();
        fetchDataPoints();
    }, 10000);
});
