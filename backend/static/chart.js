let usageHistoryChart = null;

export function updateUsageHistoryChart(snapshots) {
    const chronologicalSnapshots =
        [...snapshots].reverse();

    const labels = [];
    const cpuValues = [];
    const ramValues = [];
    const diskValues = [];

    for (const item of chronologicalSnapshots) {
        labels.push(
            item.timestamp.slice(11)
        );

        cpuValues.push(
            Number(item.cpu_usage_percent)
        );

        ramValues.push(
            Number(item.memory_usage_percent)
        );

        diskValues.push(
            Number(item.disk_usage_percent)
        );
    }

    if (usageHistoryChart === null) {
        const canvasElement =
            document.getElementById(
                "usageHistoryChart"
            );

        usageHistoryChart = new Chart(
            canvasElement,
            {
                type: "line",

                data: {
                    labels: labels,

                    datasets: [
                        {
                            label: "CPU (%)",
                            data: cpuValues,
                            borderColor: "#2563eb",
                            backgroundColor: "#2563eb",
                            borderWidth: 2,
                            tension: 0.25,
                            fill: false
                        },
                        {
                            label: "RAM (%)",
                            data: ramValues,
                            borderColor: "#7c3aed",
                            backgroundColor: "#7c3aed",
                            borderWidth: 2,
                            tension: 0.25,
                            fill: false
                        },
                        {
                            label: "Dysk (%)",
                            data: diskValues,
                            borderColor: "#0891b2",
                            backgroundColor: "#0891b2",
                            borderWidth: 2,
                            tension: 0.25,
                            fill: false
                        }
                    ]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,

                    scales: {
                        y: {
                            min: 0,
                            max: 100
                        }
                    }
                }
            }
        );

        return;
    }
    usageHistoryChart.data.labels =
        labels;

    usageHistoryChart.data.datasets[0].data =
        cpuValues;

    usageHistoryChart.data.datasets[1].data =
        ramValues;

    usageHistoryChart.data.datasets[2].data =
        diskValues;

    usageHistoryChart.update();
}