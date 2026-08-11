#include "apiclient.h"

#include <windows.h>
#include <winhttp.h>


ApiClient::ApiClient(
    const std::wstring& host,
    std::uint16_t port
    )
    : host_(host),
    port_(port)
{
}


bool ApiClient::sendSnapshot(
    const std::string& jsonPayload
    ) const
{
    HINTERNET session = WinHttpOpen(
        L"PulseWatchAgent/1.0",
        WINHTTP_ACCESS_TYPE_NO_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
        );

    if (session == nullptr)
    {
        return false;
    }

    HINTERNET connection = WinHttpConnect(
        session,
        host_.c_str(),
        port_,
        0
        );

    if (connection == nullptr)
    {
        WinHttpCloseHandle(session);
        return false;
    }

    HINTERNET request = WinHttpOpenRequest(
        connection,
        L"POST",
        L"/api/v1/snapshots",
        nullptr,
        WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
        0
        );

    if (request == nullptr)
    {
        WinHttpCloseHandle(connection);
        WinHttpCloseHandle(session);
        return false;
    }

    const wchar_t* headers =
        L"Content-Type: application/json\r\n";

    std::string payload = jsonPayload;

    const DWORD payloadSize =
        static_cast<DWORD>(payload.size());

    const BOOL sent = WinHttpSendRequest(
        request,
        headers,
        static_cast<DWORD>(-1L),
        payload.data(),
        payloadSize,
        payloadSize,
        0
        );
    BOOL responseReceived = FALSE;

    if (sent)
    {
        responseReceived =
            WinHttpReceiveResponse(request, nullptr);
    }

    DWORD statusCode = 0;
    DWORD statusCodeSize = sizeof(statusCode);
    BOOL statusCodeRead = FALSE;

    if (responseReceived)
    {
        statusCodeRead = WinHttpQueryHeaders(
            request,
            WINHTTP_QUERY_STATUS_CODE |
                WINHTTP_QUERY_FLAG_NUMBER,
            WINHTTP_HEADER_NAME_BY_INDEX,
            &statusCode,
            &statusCodeSize,
            WINHTTP_NO_HEADER_INDEX
            );
    }

    WinHttpCloseHandle(request);
    WinHttpCloseHandle(connection);
    WinHttpCloseHandle(session);

    return sent &&
           responseReceived &&
           statusCodeRead &&
           statusCode >= 200 &&
           statusCode < 300;
}
