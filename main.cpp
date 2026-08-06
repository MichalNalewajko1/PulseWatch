#include <iostream>
#include <cstdint>
#include <iomanip>
#include <chrono>
#include <thread>

#include "systemmetrics.h"
#include "csvlogger.h"

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
    CsvLogger csvLogger("pulsewatch_metrics.csv");

    const string diskPath = "C:\\";

    cout << fixed << setprecision(2);

    systemMetrics.getCpuUsage();

    while (true)
    {
        sleep_for(seconds(1));

        const SystemSnapshot snapshot =
            systemMetrics.collectSnapshot(diskPath);


        if (snapshot.computerName.empty())
        {
            cerr << "Nie udalo sie pobrac nazwy komputera.\n";
            return 1;
        }

        if (snapshot.memory.totalBytes == 0)
        {
            cerr << "Nie udalo sie pobrac informacji o pamieci.\n";
            return 1;
        }

        if (snapshot.disk.totalBytes == 0)
        {
            cerr << "Nie udalo sie pobrac informacji o dysku.\n";
            return 1;
        }

        if (snapshot.timestamp.empty())
        {
            cerr << "Nie udalo sie pobrac aktualnego czasu.\n";
            return 1;
        }
        if (!csvLogger.append(snapshot))
        {
            cerr << "Nie udalo sie zapisac pomiaru do pliku CSV.\n";
            return 1;
        }

        cout << "Czas pomiaru: "
             << snapshot.timestamp << "\n";

        cout << "Nazwa komputera: "
             << snapshot.computerName << "\n";

        cout << "Wykorzystanie CPU: "
             << snapshot.cpuUsage << "%\n";

        cout << "Calkowity RAM: "
             << bytesToGibibytes(snapshot.memory.totalBytes) << " GiB\n";

        cout << "Dostepny RAM: "
             << bytesToGibibytes(snapshot.memory.availableBytes) << " GiB\n";

        cout << "Uzywany RAM: "
             << bytesToGibibytes(snapshot.memory.usedBytes) << " GiB\n";

        cout << "Wykorzystanie RAM: "
             << snapshot.memory.usagePercent << "%\n";

        cout << "Dysk " << diskPath << "\n";

        cout << "Calkowita pojemnosc: "
             << bytesToGibibytes(snapshot.disk.totalBytes) << " GiB\n";

        cout << "Wolne miejsce: "
             << bytesToGibibytes(snapshot.disk.freeBytes) << " GiB\n";

        cout << "Zajete miejsce: "
             << bytesToGibibytes(snapshot.disk.usedBytes) << " GiB\n";

        cout << "Wykorzystanie dysku: "
             << snapshot.disk.usagePercent << "%\n";

        cout << "------------------------------\n";
        cout.flush();
    }
}