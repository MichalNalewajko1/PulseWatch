#include "systemmetrics.h"
#include <windows.h>

MemoryInfo SystemMetrics::getMemoryInfo() const
{
    MEMORYSTATUSEX memoryStatus{};
    memoryStatus.dwLength = sizeof(memoryStatus);
    BOOL success = GlobalMemoryStatusEx(&memoryStatus);

    if (!success)
    {
        return {};
    }

    MemoryInfo info{};

    info.totalBytes = memoryStatus.ullTotalPhys;
    info.availableBytes = memoryStatus.ullAvailPhys;
    info.usedBytes = info.totalBytes - info.availableBytes;

    if (info.totalBytes > 0)
    {
        info.usagePercent =
            (static_cast<double>(info.usedBytes) /
             static_cast<double>(info.totalBytes)) * 100.0;
    }

    return info;
}