from typing import Callable
from uuid import uuid4

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.http import Http404, HttpRequest, HttpResponse


class AsyncMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response: Callable):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        return response


class RestrictStaffToAdminMiddleware:
    """
    A middleware that restricts staff members access to administration panels.
    """

    def process_request(self, request: HttpRequest) -> None:
        protected_routes = ["auth/group"]
        if (
            any(request.path.endswith(url) for url in protected_routes)
            and not request.user.is_superuser
        ):
            raise Http404


class RequestIdMiddleware:
    """If X-Request-ID is missing from headers - add generated uuid as Request-ID ."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.headers.get("x-request-id", uuid4())
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response
