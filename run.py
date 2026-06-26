import sys
try:
    import flask.cli
    flask.cli.show_server_banner = lambda *x: None
except Exception:
    pass

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
