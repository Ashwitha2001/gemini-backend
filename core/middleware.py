from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


class JWTValidationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  

        token = auth_header.split(" ")[1]

        try:
            AccessToken(token)
        except TokenError as e:
            return Response(
                {
                    "error": {
                        "code": "TOKEN_EXPIRED",
                        "message": "Your session has expired. Please login again."
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception:
            return Response(
                {
                    "error": {
                        "code": "INVALID_TOKEN",
                        "message": "Invalid authentication token."
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return None
