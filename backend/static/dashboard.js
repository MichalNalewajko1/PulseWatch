import { fetchSnapshots } from "./api.js";
import { updateUsageHistoryChart } from "./chart.js";
import { updateHistoryTable, renderLatestSnapshot } from "./ui.js";

let latestDisplayedId = 0;
let refreshIntervalId = null;
let selectedChartLimit = 10;
let isLoadingSnapshots = false;
async function loadLatestSnapshot() {
    if(isLoadingSnapshots) {
        return;
    }
    isLoadingSnapshots = true;
    const historyBodyElement =
        document.getElementById("historyBody");
    const statusElement =
        document.getElementById("status");
    try {
        const snapshots =
            await fetchSnapshots(selectedChartLimit);

        if (snapshots.length === 0) {
            statusElement.textContent =
                "Brak pomiarów w bazie.";

            statusElement.className =
                "status-stale";

            return;
        }

        const snapshot = snapshots[0];
        updateUsageHistoryChart(snapshots);

        latestDisplayedId = updateHistoryTable(historyBodyElement,snapshots,latestDisplayedId);

        renderLatestSnapshot(snapshot)
    }
    catch (error) {
        statusElement.textContent =
            `API niedostępne: ${error.message}`;

        statusElement.className =
            "status-error";
    }
    finally{
        isLoadingSnapshots = false;
    }
}

const refreshButton =
    document.getElementById("refreshButton");

const chartLimitElement =
    document.getElementById("chartLimit");

function startDashboardRefresh() {
    refreshButton.textContent = "Wstrzymaj odświeżanie";

    loadLatestSnapshot();

    refreshIntervalId = setInterval(loadLatestSnapshot, 1000);
}

function stopDashboardRefresh() {
    clearInterval(refreshIntervalId);

    refreshIntervalId = null;

    refreshButton.textContent =
        "Wznów odświeżanie";

    const statusElement =
        document.getElementById("status");

    statusElement.textContent =
        "Odświeżanie dashboardu wstrzymane.";

    statusElement.className =
        "status-paused";
}

refreshButton.addEventListener("click",
    function () {
        if (refreshIntervalId === null) {
            startDashboardRefresh();
        }
        else {
            stopDashboardRefresh();
        }
    }
);

chartLimitElement.addEventListener("change",
    function () {
        selectedChartLimit =
            Number(chartLimitElement.value);

        loadLatestSnapshot();
    }
);

startDashboardRefresh();