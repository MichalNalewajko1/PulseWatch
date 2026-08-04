#include "systemmetrics.h"
#include <windows.h>

namespace
{

std::uint64_t fileTimeToUint64(const FILETIME& fileTime)
{
    ULARGE_INTEGER value{};

    value.LowPart = fileTime.dwLowDateTime;
    value.HighPart = fileTime.dwHighDateTime;

    return value.QuadPart;
}

}

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
DiskInfo SystemMetrics::getDiskInfo(
    const std::string& drivePath) const
{
    ULARGE_INTEGER freeBytesAvailable{};
    ULARGE_INTEGER totalBytes{};

    BOOL success = GetDiskFreeSpaceExA(
        drivePath.c_str(),
        &freeBytesAvailable,
        &totalBytes,
        nullptr
        );

    if (!success)
    {
        return {};
    }

    DiskInfo info{};

    info.totalBytes = totalBytes.QuadPart;
    info.freeBytes = freeBytesAvailable.QuadPart;
    info.usedBytes = info.totalBytes - info.freeBytes;

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

double SystemMetrics::getCpuUsage()
{
    FILETIME idleTime{};
    FILETIME kernelTime{};
    FILETIME userTime{};

    BOOL success = GetSystemTimes(
        &idleTime,
        &kernelTime,
        &userTime
        );

    if (!success)
    {
        return 0.0;
    }

    const std::uint64_t idle =
        fileTimeToUint64(idleTime);

    const std::uint64_t kernel =
        fileTimeToUint64(kernelTime);

    const std::uint64_t user =
        fileTimeToUint64(userTime);

    if (!hasPreviousCpuSample)
    {
        previousIdleTime = idle;
        previousKernelTime = kernel;
        previousUserTime = user;

        hasPreviousCpuSample = true;

        return 0.0;
    }

    const std::uint64_t idleDifference =
        idle - previousIdleTime;

    const std::uint64_t kernelDifference =
        kernel - previousKernelTime;

    const std::uint64_t userDifference =
        user - previousUserTime;

    previousIdleTime = idle;
    previousKernelTime = kernel;
    previousUserTime = user;

    const std::uint64_t totalDifference =
        kernelDifference + userDifference;

    if (totalDifference == 0)
    {
        return 0.0;
    }

    const std::uint64_t busyDifference =
        totalDifference - idleDifference;

    return
        (static_cast<double>(busyDifference) /
         static_cast<double>(totalDifference)) * 100.0;
}

SystemSnapshot SystemMetrics::collectSnapshot(
    const std::string& drivePath)
{
    SystemSnapshot snapshot{};

    snapshot.computerName = getComputerName();
    snapshot.cpuUsage = getCpuUsage();
    snapshot.memory = getMemoryInfo();
    snapshot.disk = getDiskInfo(drivePath);

    return snapshot;
}