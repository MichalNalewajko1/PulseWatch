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

std::string SystemMetrics::getComputerName() const
{
    char buffer[MAX_COMPUTERNAME_LENGTH + 1]{};

    DWORD size = MAX_COMPUTERNAME_LENGTH + 1;

    BOOL success = GetComputerNameA(buffer, &size);

    if (!success)
    {
        return {};
    }

    return std::string(buffer, size);
}