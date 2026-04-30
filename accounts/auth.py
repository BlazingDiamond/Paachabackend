import json
from functools import wraps

from django.http import JsonResponse
from django.utils import timezone

from .models import FrontendAuthToken


def parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return None


def token_auth_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return JsonResponse({"detail": "Authorization token missing."}, status=401)

        token_key = header.replace("Bearer ", "", 1).strip()
        token = FrontendAuthToken.objects.select_related("user").filter(key=token_key).first()
        if not token:
            return JsonResponse({"detail": "Invalid token."}, status=401)

        token.last_used_at = timezone.now()
        token.save(update_fields=["last_used_at"])
        request.auth_user = token.user
        request.auth_token = token
        return view_func(request, *args, **kwargs)

    return wrapper
