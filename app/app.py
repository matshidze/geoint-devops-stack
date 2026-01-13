import os
from flask import Flask, render_template, request, redirect
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from app.db import db, database_uri
from app.models import Submission

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQ_LATENCY = Histogram("http_request_latency_seconds", "Request latency", ["endpoint"])

def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" if testing else database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.before_request
    def _start_timer():
        request._prom_timer = REQ_LATENCY.labels(endpoint=request.path).time()

    @app.after_request
    def _record_metrics(response):
        try:
            request._prom_timer.observe_duration()
        except Exception:
            pass
        REQUESTS.labels(method=request.method, endpoint=request.path, status=str(response.status_code)).inc()
        return response

    @app.get("/")
    def index():
        submissions = (Submission.query.order_by(Submission.created_at.desc()).limit(5).all())
        return render_template("index.html", submissions=submissions)

    @app.post("/submit")
    def submit():
        text = (request.form.get("text") or "").strip()
        if text:
            db.session.add(Submission(text=text))
            db.session.commit()
        return redirect("/")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    @app.get("/metrics")
    def metrics():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    return app

#app = create_app(testing=False)


def create_app_for_gunicorn():
    return create_app(testing=False)


if __name__ == "__main__":
    import os
    # Bind safely: default to 127.0.0.1 for local dev; override via APP_HOST in containers.
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "5000"))
    create_app(testing=False).run(host=host, port=port)

