from flask import request, send_from_directory
from app_instance import FRONTEND_DIST_DIR, app


from APIs.Users import *  # noqa: E402,F401,F403
from APIs.Events import *  # noqa: E402,F401,F403
from APIs.Persons import *  # noqa: E402,F401,F403
from APIs.Attendees import *  # noqa: E402,F401,F403


def _frontend_build_missing():
    return (
        "Frontend build not found. Run `npm run build` inside the `frontend` folder first.",
        503,
    )


def _serve_frontend_entry():
    if not FRONTEND_DIST_DIR.exists():
        return _frontend_build_missing()
    return send_from_directory(FRONTEND_DIST_DIR, "index.html")


def _client_prefers_html():
    best_match = request.accept_mimetypes.best_match(["application/json", "text/html"])
    return (
        best_match == "text/html"
        and request.accept_mimetypes[best_match]
        > request.accept_mimetypes["application/json"]
    )


def _register_api_aliases():
    existing_rules = {rule.rule for rule in app.url_map.iter_rules()}

    for rule in list(app.url_map.iter_rules()):
        if rule.rule.startswith("/static") or rule.rule.startswith("/api"):
            continue

        api_rule = f"/api{rule.rule}"
        if api_rule in existing_rules:
            continue

        methods = sorted(rule.methods - {"HEAD", "OPTIONS"})
        app.add_url_rule(
            api_rule,
            endpoint=f"api_alias_{rule.endpoint}",
            view_func=app.view_functions[rule.endpoint],
            methods=methods,
        )
        existing_rules.add(api_rule)


_register_api_aliases()


@app.before_request
def serve_spa_for_browser_routes():
    if request.method != "GET":
        return None

    if request.path.startswith("/api") or request.path.startswith("/static"):
        return None

    if not _client_prefers_html():
        return None

    path = request.path.lstrip("/")
    requested_file = FRONTEND_DIST_DIR / path

    if path and requested_file.is_file():
        return send_from_directory(FRONTEND_DIST_DIR, path)

    return _serve_frontend_entry()


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path.startswith("api/"):
        return ("Not Found", 404)

    if not FRONTEND_DIST_DIR.exists():
        return _frontend_build_missing()

    requested_file = FRONTEND_DIST_DIR / path
    if path and requested_file.is_file():
        return send_from_directory(FRONTEND_DIST_DIR, path)

    return _serve_frontend_entry()

if __name__ == "__main__":
    app.run(host="localhost", port=5050, debug=True)
