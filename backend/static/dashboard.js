function bytesToGibibytes(bytes) {
    const bytesPerGibibyte =
        1024 * 1024 * 1024;

    return Number(bytes) / bytesPerGibibyte;
}
function updateAgentStatus(
    statusElement,
    timestamp
) {
    const normalizedTimestamp =
        timestamp.replace(" ", "T");

    const measurementTime =
        new Date(normalizedTimestamp);

    if (Number.isNaN(measurementTime.getTime())) {
        statusElement.textContent =
            "Nieprawidłowy czas pomiaru.";

        statusElement.className =
            "status-error";

        return;
    }

    const ageMilliseconds =
        Date.now() - measurementTime.getTime();

    const ageSeconds = Math.max(
        0,
        Math.floor(ageMilliseconds / 1000)
    );

    if (ageSeconds <= 5) {
        statusElement.textContent =
            "Agent online — dane aktualne.";

        statusElement.className =
            "status-online";
    }
    else {
        statusElement.textContent =
            `Agent nieaktywny — ostatni pomiar ${ageSeconds} s temu.`;

        statusElement.className =
            "status-stale";
    }
}
function updateMetricState(
    cardElement,
    value,
    warningThreshold,
    criticalThreshold
) {
    cardElement.classList.remove(
        "metric-warning",
        "metric-critical"
    );

    if (value >= criticalThreshold) {
        cardElement.classList.add(
            "metric-critical"
        );

        return;
    }

    if (value >= warningThreshold) {
        cardElement.classList.add(
            "metric-warning"
        );
    }
}
let latestDisplayedId = 0;
async function loadLatestSnapshot() {
    const historyBodyElement =
        document.getElementById("historyBody");
    const statusElement =
        document.getElementById("status");

    const computerNameElement =
        document.getElementById("computerName");

    const timestampElement =
        document.getElementById("timestamp");

    const cpuUsageElement =
        document.getElementById("cpuUsage");

    const ramUsageElement =
        document.getElementById("ramUsage");

    const diskUsageElement =
        document.getElementById("diskUsage");

    const ramDetailsElement =
        document.getElementById("ramDetails");

    const diskDetailsElement =
        document.getElementById("diskDetails");

    const cpuProgressElement =
        document.getElementById("cpuProgress");

    const ramProgressElement =
        document.getElementById("ramProgress");

    const diskProgressElement =
        document.getElementById("diskProgress");

    const cpuCardElement =
        document.getElementById("cpuCard");
    const ramCardElement =
        document.getElementById("ramCard");
    const diskCardElement =
        document.getElementById("diskCard");

    try {
        const response = await fetch(
            "/api/v1/snapshots?limit=10",
            {
                cache: "no-store"
            }
        );

        if (!response.ok) {
            throw new Error(
                `Błąd HTTP: ${response.status}`
            );
        }

        const snapshots = await response.json();

        if (snapshots.length === 0) {
            statusElement.textContent =
                "Brak pomiarów w bazie.";

            statusElement.className =
                "status-stale";

            return;
        }

        const snapshot = snapshots[0];
        const newSnapshots = [];

        for (const item of snapshots) {
            if (item.id > latestDisplayedId) {
                newSnapshots.push(item);
            }
        }

        newSnapshots.reverse();

        for (const item of newSnapshots) {
            const row = document.createElement("tr");

            const timestampCell =
                document.createElement("td");

            const computerNameCell =
                document.createElement("td");

            const cpuCell =
                document.createElement("td");

            const ramCell =
                document.createElement("td");

            const diskCell =
                document.createElement("td");

            timestampCell.textContent =
                item.timestamp;

            computerNameCell.textContent =
                item.computer_name;

            cpuCell.textContent =
                `${Number(item.cpu_usage_percent).toFixed(2)}%`;

            ramCell.textContent =
                `${Number(item.memory_usage_percent).toFixed(2)}%`;

            diskCell.textContent =
                `${Number(item.disk_usage_percent).toFixed(2)}%`;

            row.appendChild(timestampCell);
            row.appendChild(computerNameCell);
            row.appendChild(cpuCell);
            row.appendChild(ramCell);
            row.appendChild(diskCell);

            historyBodyElement.prepend(row);
        }

        latestDisplayedId = snapshots[0].id;

        while (historyBodyElement.children.length > 10) {
            historyBodyElement.lastElementChild.remove();
        }

        updateAgentStatus(
            statusElement,
            snapshot.timestamp
        );

        computerNameElement.textContent =
            snapshot.computer_name;

        timestampElement.textContent =
            snapshot.timestamp;

        const cpuUsage =
            Number(snapshot.cpu_usage_percent);

        const ramUsage =
            Number(snapshot.memory_usage_percent);

        const diskUsage =
            Number(snapshot.disk_usage_percent);

        updateMetricState(cpuCardElement,cpuUsage,70,90);

        updateMetricState(ramCardElement,ramUsage,75,90);

        updateMetricState(diskCardElement,diskUsage,80,90);

        cpuUsageElement.textContent =
            `${cpuUsage.toFixed(2)}%`;

        ramUsageElement.textContent =
            `${ramUsage.toFixed(2)}%`;

        diskUsageElement.textContent =
            `${diskUsage.toFixed(2)}%`;

        cpuProgressElement.value = cpuUsage;
        ramProgressElement.value = ramUsage;
        diskProgressElement.value = diskUsage;
        const ramUsed =
            bytesToGibibytes(snapshot.memory_used_bytes);

        const ramTotal =
            bytesToGibibytes(snapshot.memory_total_bytes);

        const diskUsed =
            bytesToGibibytes(snapshot.disk_used_bytes);

        const diskTotal =
            bytesToGibibytes(snapshot.disk_total_bytes);

        ramDetailsElement.textContent =
            `${ramUsed.toFixed(2)} z ${ramTotal.toFixed(2)} GiB`;

        diskDetailsElement.textContent =
            `${diskUsed.toFixed(2)} z ${diskTotal.toFixed(2)} GiB`;
    }
    catch (error) {
        statusElement.textContent =
            `API niedostępne: ${error.message}`;

        statusElement.className =
            "status-error";
    }
}

loadLatestSnapshot();
setInterval(
    loadLatestSnapshot,
    1000
);