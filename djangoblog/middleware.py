from django.http import Http404


class RestrictStaffToAdminMiddleware:
    """
    A middleware that restricts staff members access to administration panels.
    """

    def process_request(self, request):
        protected_routes = ["auth/group"]
        if (
            any(request.path.endswith(url) for url in protected_routes)
            and not request.user.is_superuser
        ):
            raise Http404
