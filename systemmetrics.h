#ifndef SYSTEMMETRICS_H
#define SYSTEMMETRICS_H

#include <cstdint>
#include <string>
struct DiskInfo
{
    std::uint64_t totalBytes = 0;
    std::uint64_t freeBytes = 0;
    std::uint64_t usedBytes = 0;
    double usagePercent = 0.0;
};

struct MemoryInfo{
    uint64_t totalBytes = 0;
    uint64_t availableBytes = 0;
    uint64_t usedBytes = 0;
    double usagePercent = 0.0;
};

struct SystemSnapshot
{
    std::string timestamp;
    std::string computerName;
    double cpuUsage = 0.0;
    MemoryInfo memory;
    DiskInfo disk;
};

class SystemMetrics
{
public:
    MemoryInfo getMemoryInfo() const;
    DiskInfo getDiskInfo(const std::string& drivePath) const;
    std::string getComputerName() const;
    double getCpuUsage();
    SystemSnapshot collectSnapshot(const std::string& drivePath);

private:
    std::uint64_t previousIdleTime = 0;
    std::uint64_t previousKernelTime = 0;
    std::uint64_t previousUserTime = 0;

    bool hasPreviousCpuSample = false;
};

#endif // SYSTEMMETRICS_H
