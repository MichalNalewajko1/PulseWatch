#include <iostream>
#include <cstdint>
#include <iomanip>
#include <chrono>
#include <thread>

#include "systemmetrics.h"

using std::cerr;
using std::cout;
using std::fixed;
using std::setprecision;
using std::uint64_t;
using std::string;
using std::chrono::seconds;
using std::this_thread::sleep_for;

double bytesToGibibytes(uint64_t bytes)
{
    constexpr double bytesPerGibibyte =
        1024.0 * 1024.0 * 1024.0;

    return static_cast<double>(bytes) / bytesPerGibibyte;
}

int main()
{
    SystemMetrics systemMetrics;
    const string computerName = systemMetrics.getComputerName();

    if (computerName.empty())
    {
        cerr << "Nie udalo sie pobrac nazwy komputera.\n";
        return 1;
    }
    cout << fixed << setprecision(2);

    cout << "Nazwa komputera: " << computerName << "\n\n";

    // Pierwsza próbka CPU zapisuje wartości początkowe.
    systemMetrics.getCpuUsage();

    while (true)
    {
        sleep_for(seconds(1));

        const double cpuUsage = systemMetrics.getCpuUsage();
        const MemoryInfo memoryInfo = systemMetrics.getMemoryInfo();

        if (memoryInfo.totalBytes == 0)
        {
            cerr << "Nie udalo sie pobrac informacji o pamieci.\n";
            return 1;
        }

        cout << "Wykorzystanie CPU: " << cpuUsage << "%\n";

        cout << "Calkowity RAM: "
             << bytesToGibibytes(memoryInfo.totalBytes) << " GiB\n";

        cout << "Dostepny RAM: "
             << bytesToGibibytes(memoryInfo.availableBytes) << " GiB\n";

        cout << "Uzywany RAM: "
             << bytesToGibibytes(memoryInfo.usedBytes) << " GiB\n";

        cout << "Wykorzystanie RAM: "
             << memoryInfo.usagePercent << "%\n";

        cout << "------------------------------\n";
        cout.flush();
    }
}