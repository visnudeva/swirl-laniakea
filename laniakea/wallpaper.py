# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import configparser
import shutil
import subprocess
from pathlib import Path


def update_waypaper_config(image: Path) -> None:
    """Remember the image for next login. Do not let waypaper re-launch swaybg."""
    conf = Path.home() / ".config" / "waypaper" / "config.ini"
    if not conf.is_file():
        return
    parser = configparser.ConfigParser()
    parser.read(conf)
    if "Settings" not in parser:
        parser["Settings"] = {}
    parser["Settings"]["wallpaper"] = str(image)
    parser["Settings"]["backend"] = "swaybg"
    # PNG is already exact output size with contain framing baked in.
    parser["Settings"]["fill"] = "fill"
    conf.parent.mkdir(parents=True, exist_ok=True)
    with conf.open("w", encoding="utf-8") as fh:
        parser.write(fh)


def apply_with_swaybg(image: Path) -> None:
    """Show the monitor-baked PNG. fill is 1:1 (no extra crop/zoom)."""
    image = image.resolve()
    if not shutil.which("swaybg"):
        raise RuntimeError("swaybg is not available")

    # Drive swaybg ourselves. waypaper --wallpaper often forces fill on a
    # non-baked image and re-introduces crop-zoom.
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
