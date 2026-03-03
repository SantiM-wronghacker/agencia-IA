"""
Agencia IA - Health Check Service

Provides health check endpoints for all services.
Can run standalone as a health monitor service on port 9101.
"""

import logging
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import Any

logger = logging.getLogger("agencia.health")


def check_service_health(host: str, port: int, path: str = "/health") -> dict[str, Any]:
    """Check health of a single service via HTTP."""
    import urllib.request
    import urllib.error

    url = f"http://{host}:{port}{path}"
    start = time.monotonic()
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            duration_ms = (time.monotonic() - start) * 1000
            return {
                "service": f"{host}:{port}",
                "status": "healthy",
                "response_code": resp.status,
                "duration_ms": round(duration_ms, 2),
            }
    except Exception as exc:
        duration_ms = (time.monotonic() - start) * 1000
        return {
            "service": f"{host}:{port}",
            "status": "unhealthy",
            "error": str(exc),
            "duration_ms": round(duration_ms, 2),
        }


def check_all_services() -> dict[str, Any]:
    """Check health of all known services."""
    services = [
        ("api_agencia", 8000, "/health"),
        ("dashboard_web", 8080, "/health"),
        ("app_dashboard", 5000, "/health"),
        ("app_streamlit", 8501, "/_stcore/health"),
    ]

    results = {}
    all_healthy = True

    for host, port, path in services:
        result = check_service_health(host, port, path)
        results[host] = result
        if result["status"] != "healthy":
            all_healthy = False

    return {
        "overall_status": "healthy" if all_healthy else "degraded",
        "services": results,
        "timestamp": time.time(),
    }


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP handler for health check endpoint."""

    def do_GET(self) -> None:
        if self.path == "/health":
            response = {"status": "healthy", "service": "health_monitor"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/check":
            response = check_all_services()
            status_code = 200 if response["overall_status"] == "healthy" else 503
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        logger.debug(format, *args)


def run_health_server(port: int = 9101) -> None:
    """Run standalone health check server."""
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info("health_monitor_started", extra={"port": port})
    server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_health_server(int(os.environ.get("HEALTH_PORT", "9101")))
