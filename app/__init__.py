from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dbvc-website-secret"
    app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB

    from app.routes.home import home_bp
    from app.routes.demo import demo_bp
    from app.routes.download import download_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(demo_bp)
    app.register_blueprint(download_bp)

    return app
