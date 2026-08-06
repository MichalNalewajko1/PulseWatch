#ifndef CSVLOGGER_H
#define CSVLOGGER_H

#include "systemmetrics.h"

#include <string>

class CsvLogger
{
public:
    explicit CsvLogger(const std::string& filePath);

    bool append(const SystemSnapshot& snapshot) const;

private:
    std::string filePath_;
};

#endif // CSVLOGGER_H