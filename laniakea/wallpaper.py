# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import configparser
import shutil
import subprocess
from pathlib import Path

# Match the in-app letterboxed preview: show the whole image, do not crop-zoom.
_SWAYBG_MODE = "fit"


def update_waypaper_config(image: Path) -> None:
    """Point waypaper at the new image so the next login restore keeps it."""
    conf = Path.home() / ".config" / "waypaper" / "config.ini"
    if not conf.is_file():
        return
    parser = configparser.ConfigParser()
    parser.read(conf)
    if "Settings" not in parser:
        parser["Settings"] = {}
    parser["Settings"]["wallpaper"] = str(image)
    parser["Settings"]["backend"] = "swaybg"
    parser["Settings"]["fill"] = _SWAYBG_MODE
    conf.parent.mkdir(parents=True, exist_ok=True)
    with conf.open("w", encoding="utf-8") as fh:
        parser.write(fh)


def apply_with_swaybg(image: Path) -> None:
    """Set the image with swaybg fit (full artwork, no crop-zoom)."""
    image = image.resolve()

    # Always drive swaybg ourselves with an explicit mode. waypaper's CLI
    # often reapplies "fill" from an old config and re-introduces the zoom.
    if not shutil.which("swaybg"):
        raise RuntimeError("swaybg is not available")

    subprocess.run(["pkill", "-x", "swaybg"], check=False)
    subprocess.Popen(
        ["swaybg", "-i", str(image), "-m", _SWAYBG_MODE],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    update_waypaper_config(image)


def save_png_bytes(data: bytes, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest
