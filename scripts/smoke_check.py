from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.data_access import load_learning_bundle  # noqa: E402
from utils.integrity import write_json  # noqa: E402

REPORT_FILE = BASE_DIR / "data" / "meta" / "smoke_check_report.json"
REQUIRED_ENDPOINTS = {
    "home": "/",
    "champion_guide": "/guide",
    "matchups_overview": "/matchups",
    "learning": "/learning",
}
LOCALES = ("pt-BR", "en")
REQUIRED_TEMPLATES = [
    "templates/base.html",
    "templates/home.html",
    "templates/champion_guide.html",
    "templates/learning.html",
    "templates/matchups_overview.html",
]


def _flask_available() -> bool:
    return importlib.util.find_spec("flask") is not None


def _app_py_compile_ok() -> bool:
    try:
        py_compile.compile(str(BASE_DIR / "app.py"), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def _static_fallback_report() -> dict:
    app_py = (BASE_DIR / "app.py").read_text(encoding="utf-8")
    endpoint_presence = {
        endpoint: route in app_py for endpoint, route in REQUIRED_ENDPOINTS.items()
    }
    templates = {
        relative: (BASE_DIR / relative).exists() for relative in REQUIRED_TEMPLATES
    }
    learning_bundle = load_learning_bundle()
    learning_ok = bool(learning_bundle.get("sections")) and bool(learning_bundle.get("overview"))
    app_py_compile_ok = _app_py_compile_ok()
    smoke_ok = app_py_compile_ok and all(endpoint_presence.values()) and all(templates.values()) and learning_ok
    return {
        "runtime_mode": "static_fallback_no_flask_installed",
        "imports_ok": app_py_compile_ok,
        "app_py_compile_ok": app_py_compile_ok,
        "dependency_warning": "Flask is not installed in the current validation container.",
        "endpoint_strings_present": endpoint_presence,
        "templates_present": templates,
        "learning_bundle_safe": learning_ok,
        "learning_sections_count": len(learning_bundle.get("sections", [])),
        "translations_mode_checked": list(LOCALES),
        "smoke_ok": smoke_ok,
    }


def _runtime_report() -> dict:
    from app import app  # noqa: E402

    routes = {rule.endpoint: rule.rule for rule in app.url_map.iter_rules()}
    missing_endpoints = sorted([name for name in REQUIRED_ENDPOINTS if name not in routes])

    statuses = {}
    client = app.test_client()
    for endpoint, path in REQUIRED_ENDPOINTS.items():
        locale_status = {}
        for locale in LOCALES:
            response = client.get(f"{path}?lang={locale}")
            locale_status[locale] = {
                "status_code": response.status_code,
                "ok": response.status_code == 200,
            }
        statuses[endpoint] = {
            "path": path,
            "locales": locale_status,
            "ok": all(item["ok"] for item in locale_status.values()),
        }

    learning_bundle = load_learning_bundle()
    learning_ok = bool(learning_bundle.get("sections")) and bool(learning_bundle.get("overview"))

    return {
        "runtime_mode": "flask_runtime",
        "imports_ok": True,
        "app_py_compile_ok": True,
        "missing_endpoints": missing_endpoints,
        "routes_checked": statuses,
        "learning_bundle_safe": learning_ok,
        "learning_sections_count": len(learning_bundle.get("sections", [])),
        "translations_mode_checked": list(LOCALES),
        "smoke_ok": not missing_endpoints and all(item["ok"] for item in statuses.values()) and learning_ok,
    }


def main() -> int:
    report = _runtime_report() if _flask_available() else _static_fallback_report()
    write_json(REPORT_FILE, report)

    if report["smoke_ok"]:
        print(f"Smoke check passed. Report written to {REPORT_FILE}")
        if report.get("dependency_warning"):
            print(report["dependency_warning"])
        return 0

    print(f"Smoke check failed. Report written to {REPORT_FILE}")
    if report.get("dependency_warning"):
        print(report["dependency_warning"])
    if "missing_endpoints" in report and report["missing_endpoints"]:
        print("Missing endpoints:")
        for endpoint in report["missing_endpoints"]:
            print(f" - {endpoint}")
    if "routes_checked" in report:
        for endpoint, status in report["routes_checked"].items():
            if not status["ok"]:
                for locale, locale_status in status["locales"].items():
                    if not locale_status["ok"]:
                        print(f" - {endpoint} [{locale}]: HTTP {locale_status['status_code']}")
    if "endpoint_strings_present" in report:
        for endpoint, present in report["endpoint_strings_present"].items():
            if not present:
                print(f" - endpoint string missing: {endpoint}")
    if not report["learning_bundle_safe"]:
        print(" - learning bundle is not safe for runtime")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
