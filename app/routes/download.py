import os
from flask import Blueprint, send_from_directory, abort

download_bp = Blueprint("download", __name__)

DOWNLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "app", "static", "downloads"
)


@download_bp.route("/download", methods=["GET"])
def download_exe():
    """Serve the DBVC Desktop .exe file for download."""
    filename = "DBVC-Desktop.exe"
    directory = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static", "downloads"
    )

    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        abort(404, description="Download file not found. Please check back later.")

    return send_from_directory(
        directory,
        filename,
        as_attachment=True,
        download_name="DBVC-Desktop.exe",
    )
