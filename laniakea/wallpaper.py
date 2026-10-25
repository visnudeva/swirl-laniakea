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
    # PNG is already exact output size with letterboxing baked in.
    parser["Settings"]["fill"] = "fill"
    conf.parent.mkdir(parents=True, exist_ok=True)
    with conf.open("w", encoding="utf-8") as fh:
        parser.write(fh)


def apply_with_swaybg(image: Path) -> None:
    """Show the monitor-baked PNG. fill is 1:1 (no extra crop/zoom)."""
    image = image.resolve()
    if not shutil.which("swaybg"):
        raise RuntimeError("swaybg is not available")

    subprocess.run(["pkill", "-x", "swaybg"], check=False)
    subprocess.Popen(
        ["swaybg", "-i", str(image), "-m", "fill"],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Keep waypaper in sync for the next login restore, but do not let it
    # relaunch swaybg with a different image/mode on top of us.
    update_waypaper_config(image)


def save_png_bytes(data: bytes, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest
