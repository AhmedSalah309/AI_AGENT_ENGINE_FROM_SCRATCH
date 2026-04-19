from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

# Instead of from .routes use the full path
from agent_engine.api.routes import chat_bp

# Use the absolute path because it is clearer in the Clean Architecture
from agent_engine.config.settings import settings


def create_app():
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)

    # Load settings from settings class
    app.config.from_object(settings)

    # Register the Blueprints
    app.register_blueprint(chat_bp, url_prefix="/api/v1")

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify(
            {
                "status": "healthy",
                "app": settings.APP_NAME,
                "version": settings.APP_VERSION,
            }
        ), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
