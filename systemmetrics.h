#ifndef SYSTEMMETRICS_H
#define SYSTEMMETRICS_H

#include <cstdint>
#include <string>

struct MemoryInfo{
    uint64_t totalBytes = 0;
    uint64_t availableBytes = 0;
    uint64_t usedBytes = 0;
    double usagePercent = 0.0;
};

class SystemMetrics
{
public:
    MemoryInfo getMemoryInfo() const;
    std::string getComputerName() const;
    double getCpuUsage();

private:
    std::uint64_t previousIdleTime = 0;
    std::uint64_t previousKernelTime = 0;
    std::uint64_t previousUserTime = 0;

    bool hasPreviousCpuSample = false;
};

#endif // SYSTEMMETRICS_H
