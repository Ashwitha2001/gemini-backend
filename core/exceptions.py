from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        detail = response.data.get("detail", "An error occurred")
        code = "SERVER_ERROR"

        if "not authenticated" in str(detail).lower():
            code = "AUTH_REQUIRED"
        elif "expired" in str(detail).lower():
            code = "TOKEN_EXPIRED"

        response.data = {
            "error": {
                "code": code,
                "message": str(detail)
            }
        }
    return response
