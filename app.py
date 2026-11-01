"""Nadaan Bachcha: dependency-free WSGI app with server-side password gate."""
from datetime import datetime, timezone
from email.utils import formatdate
from hashlib import sha256
import hmac
import mimetypes
import os
from pathlib import Path
import secrets
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

BASE = Path(__file__).resolve().parent
SECRET = os.environ.get("NADAAN_SECRET_KEY", "").encode("utf-8")
PASSWORD = os.environ.get("NADAAN_PASSWORD", "")
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "0") == "1"
SESSION_SECONDS = 8 * 60 * 60


def response(start_response, status, body=b"", content_type="text/plain; charset=utf-8", headers=None):
    merged = {"Content-Type": content_type, "Content-Length": str(len(body)), "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "no-referrer"}
    if headers:
        merged.update(dict(headers))
    hs = list(merged.items())
    start_response(status, hs)
    return [body]


def signed_session():
    raw = os.environ.get("HTTP_COOKIE", "")
    # WSGI servers expose request cookies through environ, not process env; handled in application().
    return False


def make_token():
    issued = str(int(datetime.now(timezone.utc).timestamp()))
    nonce = secrets.token_urlsafe(18)
    payload = f"{issued}.{nonce}"
    sig = hmac.new(SECRET, payload.encode(), sha256).hexdigest()
    return f"{payload}.{sig}"


def valid_token(token):
    try:
        issued, nonce, sig = token.split(".", 2)
        payload = f"{issued}.{nonce}"
        expected = hmac.new(SECRET, payload.encode(), sha256).hexdigest()
        age = int(datetime.now(timezone.utc).timestamp()) - int(issued)
        return 0 <= age <= SESSION_SECONDS and hmac.compare_digest(sig, expected)
    except (ValueError, TypeError):
        return False


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET").upper()
    cookie_header = environ.get("HTTP_COOKIE", "")
    token = ""
    for part in cookie_header.split(";"):
        if part.strip().startswith("nb_session="):
            token = part.strip().split("=", 1)[1]
            break
    authenticated = bool(SECRET and valid_token(token))

    if path == "/health" and method == "GET":
        return response(start_response, "200 OK", b'{"status":"ok"}', "application/json")

    if not SECRET or not PASSWORD:
        return response(start_response, "503 Service Unavailable", b"Server setup incomplete. Set NADAAN_SECRET_KEY and NADAAN_PASSWORD.")

    if path == "/" and method == "GET":
        if authenticated:
            start_response("302 Found", [("Location", "/site"), ("Content-Length", "0"), ("Cache-Control", "no-store")]); return [b""]
        page = (BASE / "templates" / "login.html").read_bytes()
        return response(start_response, "200 OK", page, "text/html; charset=utf-8")

    if path == "/login" and method == "POST":
        try:
            size = int(environ.get("CONTENT_LENGTH") or "0")
        except ValueError:
            size = 0
        if size > 4096:
            return response(start_response, "413 Payload Too Large", b"Request too large")
        raw = environ["wsgi.input"].read(size).decode("utf-8", "replace")
        candidate = parse_qs(raw).get("password", [""])[0]
        if not hmac.compare_digest(candidate.encode("utf-8"), PASSWORD.encode("utf-8")):
            return response(start_response, "401 Unauthorized", b'{"ok":false,"message":"That password doesn\'t open this little door. Try again."}', "application/json")
        cookie = f"nb_session={make_token()}; Path=/; HttpOnly; SameSite=Lax; Max-Age={SESSION_SECONDS}" + ("; Secure" if COOKIE_SECURE else "")
        return response(start_response, "200 OK", b'{"ok":true,"next":"/site"}', "application/json", [("Set-Cookie", cookie)])

    if path == "/logout" and method == "POST":
        cookie = "nb_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0" + ("; Secure" if COOKIE_SECURE else "")
        start_response("303 See Other", [("Location", "/"), ("Set-Cookie", cookie), ("Content-Length", "0"), ("Cache-Control", "no-store")]); return [b""]

    if path == "/site" and method == "GET":
        if not authenticated:
            start_response("302 Found", [("Location", "/"), ("Content-Length", "0"), ("Cache-Control", "no-store")]); return [b""]
        page = (BASE / "templates" / "site.html").read_bytes()
        return response(start_response, "200 OK", page, "text/html; charset=utf-8")

    if path.startswith("/assets/") and method in ("GET", "HEAD"):
        if not authenticated:
            return response(start_response, "404 Not Found", b"Not found")
        rel = path[len("/assets/"):]
        target = (BASE / "static" / rel).resolve()
        static_root = (BASE / "static").resolve()
        if not target.is_relative_to(static_root) or not target.is_file():
            return response(start_response, "404 Not Found", b"Not found")
        data = target.read_bytes() if method == "GET" else b""
        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        return response(start_response, "200 OK", data, mime, [("Content-Length", str(target.stat().st_size))])

    return response(start_response, "404 Not Found", b"Not found")


if __name__ == "__main__":
    if not SECRET or not PASSWORD:
        raise SystemExit("Set NADAAN_SECRET_KEY and NADAAN_PASSWORD before running.")
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    with make_server(host, port, application) as server:
        print(f"Nadaan Bachcha listening on http://{host}:{port}")
        server.serve_forever()
