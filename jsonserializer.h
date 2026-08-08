#ifndef JSONSERIALIZER_H
#define JSONSERIALIZER_H

#include "systemmetrics.h"

#include <string>

class JsonSerializer
{
public:
    std::string serialize(
        const SystemSnapshot& snapshot) const;
};

#endif // JSONSERIALIZER_H