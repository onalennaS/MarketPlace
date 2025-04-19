from django.utils.deprecation import MiddlewareMixin

class PermissionsPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Permissions-Policy'] = (
            "accelerometer=(), autoplay=(), camera=(), "
            "fullscreen=(self), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()"
        )
        return response