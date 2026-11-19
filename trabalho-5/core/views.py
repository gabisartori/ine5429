import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Note


def _parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8")), None
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, JsonResponse({"error": "JSON inválido."}, status=400)


def _authenticate_from_payload(username: str, password: str):
    if not username or not password:
        return None
    return authenticate(username=username, password=password)


@csrf_exempt
@require_POST
def create_user(request):
    data, err = _parse_json_body(request)
    if err:
        return err

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if len(username) < 3 or len(password) < 6:
        return JsonResponse(
            {"error": "Informe username (mín. 3 chars) e password (mín. 6 chars)."},
            status=400,
        )

    try:
        user = User.objects.create_user(username=username, password=password)
    except IntegrityError:
        return JsonResponse({"error": "Usuário já existe."}, status=409)

    return JsonResponse({"id": user.id, "username": user.username}, status=201)


@csrf_exempt
@require_POST
def create_note(request):
    data, err = _parse_json_body(request)
    if err:
        return err

    user = _authenticate_from_payload(
        (data.get("username") or "").strip(),
        data.get("password") or "",
    )
    if not user:
        return JsonResponse({"error": "Credenciais inválidas."}, status=401)

    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    if not title or not content:
        return JsonResponse(
            {"error": "Campos 'title' e 'content' são obrigatórios."},
            status=400,
        )

    note = Note.objects.create(owner=user, title=title, content=content)
    return JsonResponse(
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "owner": user.username,
        },
        status=201,
    )


@require_GET
def list_notes(request):
    username = (request.GET.get("username") or "").strip()
    password = request.GET.get("password") or ""

    user = _authenticate_from_payload(username, password)
    if not user:
        return JsonResponse({"error": "Credenciais inválidas."}, status=401)

    notes = [
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at.isoformat(),
        }
        for n in Note.objects.filter(owner=user).order_by("-created_at")
    ]
    return JsonResponse({"username": user.username, "notes": notes}, status=200)