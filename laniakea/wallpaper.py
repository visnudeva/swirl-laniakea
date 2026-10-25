# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import configparser
import shutil
import subprocess
from pathlib import Path


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
    # Image is already monitor-sized with letterboxing baked in, so fill is 1:1.
    parser["Settings"]["fill"] = "fill"
    conf.parent.mkdir(parents=True, exist_ok=True)
    with conf.open("w", encoding="utf-8") as fh:
        parser.write(fh)


def apply_with_swaybg(image: Path) -> None:
    """Show a monitor-baked PNG. fill is safe because the file is already 1:1."""
    image = image.resolve()
    if not shutil.which("swaybg"):
        raise RuntimeError("swaybg is not available")

    # Drop every swaybg (waypaper --restore may have left a fill instance).
    subprocess.run(["pkill", "-x", "swaybg"], check=False)
    subprocess.Popen(
        ["swaybg", "-o", "*", "-i", str(image), "-m", "fill"],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    update_waypaper_config(image)


def save_png_bytes(data: bytes, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest
