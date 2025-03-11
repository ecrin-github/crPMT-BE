class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.META.get('HTTP_AUTHORIZATION') == 'Bearer null' or
                request.META.get('HTTP_AUTHORIZATION') == 'Bearer'):
            request.META['HTTP_AUTHORIZATION'] = ''

        response = self.get_response(request)
        return response
