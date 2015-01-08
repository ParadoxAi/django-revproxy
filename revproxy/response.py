from django.http import HttpResponse

HOP_BY_HOP_HEADERS = (
    'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization',
    'te', 'trailers', 'transfer-encoding', 'upgrade')


class HttpProxyResponse(HttpResponse):

    def __init__(self, proxy_response, *args, **kwargs):
        content = proxy_response.data or b''
        headers = proxy_response.headers
        status = proxy_response.status

        content_type = headers.get('Content-Type')
        super(HttpProxyResponse, self).__init__(content, status=status,
                                                content_type=content_type,
                                                *args, **kwargs)

        for header, value in headers.items():
            if header.lower() not in HOP_BY_HOP_HEADERS:
                self[header.title()] = value
