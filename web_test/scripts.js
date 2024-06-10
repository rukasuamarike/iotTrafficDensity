document.addEventListener("DOMContentLoaded", function() {
    const apiStatsUrl = 'https://79b3-2601-647-4d83-3930-00-f3b7.ngrok-free.app/traffic-stats';
    const apiLogsUrl = 'https://79b3-2601-647-4d83-3930-00-f3b7.ngrok-free.app/vehicle-logs';
    const maxLogEntries = 50;
    let vehicleLogs = [];
    let logSet = new Set();

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
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                const text = await response.text();
                console.error("Received non-JSON response:", text);
                throw new TypeError("Received non-JSON response");
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
            document.querySelector('.current-minute-count').textContent = data.current_minute_count || 'N/A';
            document.querySelector('.current-traffic-level-text').textContent = `The current traffic level is ${data.current_minute_count || 'N/A'} vehicles per minute, which is decreasing compared to the previous period.`;
        } catch (error) {
            console.error('Error fetching traffic stats:', error);
            document.querySelector('.hourly-average').textContent = 'N/A';
            document.querySelector('.thirty-minute-average').textContent = 'N/A';
            document.querySelector('.five-minute-average').textContent = 'N/A';
            document.querySelector('.max-vehicles').textContent = 'N/A';
            document.querySelector('.min-vehicles').textContent = 'N/A';
            document.querySelector('.current-minute-count').textContent = 'N/A';
            document.querySelector('.current-traffic-level-text').textContent = 'The current traffic level is N/A vehicles per minute.';
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
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                const text = await response.text();
                console.error("Received non-JSON response:", text);
                throw new TypeError("Received non-JSON response");
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

    // Initial fetch
    fetchTrafficStats();
    fetchVehicleLogs();

    // Re-fetch every 20 seconds
    setInterval(() => {
        fetchTrafficStats();
        fetchVehicleLogs();
    }, 20000);
});
