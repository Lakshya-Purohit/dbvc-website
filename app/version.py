import subprocess
import os
import urllib.request
import json
import logging
import time

logger = logging.getLogger("dbvc_website")

_cached_version = None
_last_check_time = 0
CACHE_TTL = 3600  # Cache for 1 hour

def get_latest_version() -> str:
    """
    Retrieves the latest version tag dynamically.
    First checks local git tags for development.
    Then checks GitHub Releases API (cached).
    Then parses the desktop app configuration files.
    Finally falls back to a safe default version.
    """
    global _cached_version, _last_check_time
    
    current_time = time.time()
    if _cached_version and (current_time - _last_check_time < CACHE_TTL):
        return _cached_version

    # 1. Try local git command on the desktop folder (Development)
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        desktop_dir = os.path.abspath(os.path.join(base_dir, "..", "dbvc-desktop"))
        
        if os.path.exists(desktop_dir) and os.path.exists(os.path.join(desktop_dir, ".git")):
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                cwd=desktop_dir,
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            version = result.stdout.strip().lstrip("vV")
            if version:
                _cached_version = version
                _last_check_time = current_time
                return version
    except Exception as e:
        logger.debug("Could not retrieve version from local desktop git repository: %s", e)

    # 2. Try fetching from GitHub API as a fallback (Production/Deployment)
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/Lakshya-Purohit/dbvc-desktop/releases/latest",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "DBVC-Website-VersionChecker"
            }
        )
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            version = data.get("tag_name", "").lstrip("vV").strip()
            if version:
                _cached_version = version
                _last_check_time = current_time
                return version
    except Exception as e:
        logger.debug("Could not retrieve version from GitHub API: %s", e)

    # 3. Try parsing app/config.py from dbvc-desktop
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.abspath(os.path.join(base_dir, "..", "dbvc-desktop", "app", "config.py"))
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()
                import re
                match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    version = match.group(1)
                    _cached_version = version
                    _last_check_time = current_time
                    return version
    except Exception as e:
        logger.debug("Could not parse version from desktop config.py: %s", e)

    # 4. Final Fallback
    if _cached_version:
        return _cached_version
    return "1.0.5"
