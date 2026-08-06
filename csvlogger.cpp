#include "csvlogger.h"
#include <fstream>
#include <iomanip>

CsvLogger::CsvLogger(const std::string& filePath)
    : filePath_(filePath)
{
}

bool CsvLogger::append(const SystemSnapshot& snapshot) const
{
    std::ifstream existingFile(
        filePath_,
        std::ios::ate
        );

    const bool shouldWriteHeader =
        !existingFile.is_open() ||
        existingFile.tellg() == 0;

    existingFile.close();

    std::ofstream file(filePath_, std::ios::app);

    if (!file.is_open())
    {
        return false;
    }

    if (shouldWriteHeader)
    {
        file
            << "timestamp,"
            << "computer_name,"
            << "cpu_usage_percent,"
            << "ram_total_bytes,"
            << "ram_available_bytes,"
            << "ram_used_bytes,"
            << "ram_usage_percent,"
            << "disk_total_bytes,"
            << "disk_free_bytes,"
            << "disk_used_bytes,"
            << "disk_usage_percent\n";
    }

    file << std::fixed << std::setprecision(2);

    file
        << snapshot.timestamp << ','
        << snapshot.computerName << ','
        << snapshot.cpuUsage << ','
        << snapshot.memory.totalBytes << ','
        << snapshot.memory.availableBytes << ','
        << snapshot.memory.usedBytes << ','
        << snapshot.memory.usagePercent << ','
        << snapshot.disk.totalBytes << ','
        << snapshot.disk.freeBytes << ','
        << snapshot.disk.usedBytes << ','
        << snapshot.disk.usagePercent << '\n';

    file.flush();

    return file.good();
}