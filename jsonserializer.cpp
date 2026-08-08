#include "jsonserializer.h"

#include <nlohmann/json.hpp>

std::string JsonSerializer::serialize(
    const SystemSnapshot& snapshot) const
{
    nlohmann::json document;

    document["timestamp"] =
        snapshot.timestamp;

    document["computer_name"] =
        snapshot.computerName;

    document["cpu_usage_percent"] =
        snapshot.cpuUsage;

    document["memory"]["total_bytes"] =
        snapshot.memory.totalBytes;

    document["memory"]["available_bytes"] =
        snapshot.memory.availableBytes;

    document["memory"]["used_bytes"] =
        snapshot.memory.usedBytes;

    document["memory"]["usage_percent"] =
        snapshot.memory.usagePercent;

    document["disk"]["total_bytes"] =
        snapshot.disk.totalBytes;

    document["disk"]["free_bytes"] =
        snapshot.disk.freeBytes;

    document["disk"]["used_bytes"] =
        snapshot.disk.usedBytes;

    document["disk"]["usage_percent"] =
        snapshot.disk.usagePercent;

    return document.dump();
}