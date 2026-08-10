#ifndef APICLIENT_H
#define APICLIENT_H

#include <cstdint>
#include <string>

class ApiClient
{
public:
    ApiClient(
        const std::wstring& host,
        std::uint16_t port
        );

    bool sendSnapshot(
        const std::string& jsonPayload
        ) const;

private:
    std::wstring host_;
    std::uint16_t port_;
};

#endif // APICLIENT_H