#include "apiclient.h"

ApiClient::ApiClient(
    const std::wstring& host,
    std::uint16_t port
    )
    : host_(host),
    port_(port)
{
}