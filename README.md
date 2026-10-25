# swirl-laniakea

**Generative flow-field wallpaper for [SweetPotatOs](https://github.com/visnudeva/SweetPotatOs) / Swirl.**

Laniakea draws a relaxing particle field in a live window. Watch colours drift along a Perlin-noise vector field, pick a shape mask, then **Apply** to save a PNG and set it as your Swirl wallpaper. Opt-in — it never replaces the default Neon wallpaper until you ask.

This is the Wayland / Swirl sibling of the [GNOME Shell extension](https://github.com/visnudeva/Laniakea). Same sketch spirit and masks; no GNOME Shell required.

<p align="center">
  <img src="assets/laniakea-preview.jpg" alt="Laniakea generative flow-field preview" width="860" />
</p>

## Features

- **Generative flow-field wallpaper** — colourful particles drift along a Perlin-noise vector field
- **Live preview** — watch the pattern grow, then save exactly what you see
- **Click to regenerate** — primary-click inside the shape mask to start a new drawing
- **Shape masks** — limit where particles appear (circle, triangles, diamond, hexagon, rectangles, or full screen)
- **Apply to desktop** — writes `~/Pictures/Wallpapers/laniakea.png` and sets it with swaybg / waypaper
- **Resize-friendly** — tiling keeps the artwork (stretched to fill); it does not wipe and re-roll
- **Offline** — p5.js is vendored; no CDN required

## Customization

Use the shape dropdown in the toolbar:

| Shape | Description |
|---|---|
| Circle | Round central area (default) |
| Triangle up / down | Triangular mask |
| Diamond | Rotated square |
| Hexagon | Regular hexagon |
| Vertical / horizontal rectangle | Rectangular masks |
| Wide | Full canvas — no mask |

Extra actions (Redraw, Save PNG, Apply wallpaper) live under the ☰ menu; **Apply** stays on the bar for quick use.

## Installation

### SweetPotatOs testing channel (recommended)

```bash
sudo sweetpotatos-update --testing
laniakea
```

Or open **Laniakea** from the app menu.

### From source

Needs `python`, `python-gobject`, `gtk4`, `libadwaita`, `webkitgtk-6.0`, and `swaybg` (optional: `waypaper`).

```bash
git clone https://github.com/visnudeva/swirl-laniakea.git
cd swirl-laniakea
PYTHONPATH=. LANIAKEA_WEB_ROOT="$PWD/share/laniakea/web" python -m laniakea
```

### Arch package (SweetPotatOs packaging tree)

The SweetPotatOs repo builds `laniakea` from this source:

```bash
# from a SweetPotatOs checkout, with this tree as sibling ../laniakea
# or: LANIAKEA_SRC=/path/to/swirl-laniakea
sudo ./build.sh --build-laniakea
```

## How it works

1. A small **GTK + WebKit** app loads the vendored p5.js sketch.
2. Particles stream inside the selected **mask** while you watch.
3. **Apply** / **Save** snapshots the live canvas (WYSIWYG) and scales it to your display.
4. The PNG is stored under `~/Pictures/Wallpapers/` and handed to **waypaper** or **swaybg**.

## Requirements

- Wayland session with Swirl (or another swaybg-compatible compositor)
- Python 3 + PyGObject
- GTK 4, WebKitGTK 6.0
- swaybg (and optionally waypaper, for remembering the wallpaper across logins)

## Troubleshooting

**Apply did nothing?**

- Confirm `swaybg` or `waypaper` is installed.
- Check that `~/Pictures/Wallpapers/laniakea.png` was written.

**Click-to-regenerate not working?**

- Click inside the configured shape mask (unless **Wide** is selected).

## Related

- GNOME extension: [visnudeva/Laniakea](https://github.com/visnudeva/Laniakea)
- Distro: [visnudeva/SweetPotatOs](https://github.com/visnudeva/SweetPotatOs)

## License

GNU General Public License v3.0 or later. See [LICENSE](LICENSE) and the SPDX headers in source files.

## Contributing

Issues and pull requests are welcome at [github.com/visnudeva/swirl-laniakea](https://github.com/visnudeva/swirl-laniakea).
