from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods

from .auth import parse_json_body, token_auth_required
from .models import FrontendAuthToken

User = get_user_model()


@require_http_methods(["POST"])
def register_api(request):
    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    username = (payload.get("username") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not username or not email or not password:
        return JsonResponse({"detail": "username, email and password are required."}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "Username is already in use."}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"detail": "Email is already in use."}, status=400)

    try:
        validate_password(password)
    except ValidationError as exc:
        return JsonResponse({"detail": list(exc.messages)}, status=400)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
        is_active=True,
    )
    token = FrontendAuthToken.create_for_user(user)

    return JsonResponse(
        {
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
            },
        },
        status=201,
    )


@require_http_methods(["POST"])
def login_api(request):
    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    user = User.objects.filter(username=username, is_active=True).first()
    if not user or not user.check_password(password):
        return JsonResponse({"detail": "Invalid credentials."}, status=401)

    token = FrontendAuthToken.create_for_user(user)
    return JsonResponse(
        {
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
            },
        }
    )


@require_http_methods(["POST"])
@token_auth_required
def logout_api(request):
    request.auth_token.delete()
    return JsonResponse({"detail": "Logged out successfully."})


@require_GET
@token_auth_required
def me_api(request):
    user = request.auth_user
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
        }
    )
