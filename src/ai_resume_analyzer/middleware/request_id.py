from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from ai_resume_analyzer.constants.http import REQUEST_ID_HEADER
from ai_resume_analyzer.utils.context import reset_request_id, set_request_id
from ai_resume_analyzer.utils.request_id import generate_request_id


class RequestIDMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        header_name: str = REQUEST_ID_HEADER,
    ) -> None:
        self.app = app
        self.header_name = header_name

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        request_id = headers.get(self.header_name) or generate_request_id()
        token = set_request_id(request_id)

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_headers = MutableHeaders(scope=message)
                response_headers[self.header_name] = request_id
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            reset_request_id(token)
