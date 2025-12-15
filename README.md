# Hyprland for Fedora 43+

Unofficial Hyprland builds for Fedora 43 with latest features.

## Install from COPR

```bash
sudo dnf copr enable asherbuk/hyprland
sudo dnf install hyprland
```

## What's Included

| Package | Description |
|---------|-------------|
| hyprland | Dynamic tiling Wayland compositor |
| hyprctl | CLI control tool |
| hyprpm | Plugin manager |
| xdg-desktop-portal-hyprland | Portal for screen sharing |
| hyprland-libs | hyprlang, hyprutils, hyprcursor, hyprgraphics, aquamarine |

## Why This Repo?

Fedora 43 ships with Hyprland 0.45, but upstream is at 0.52+. This repo provides:

- Latest Hyprland releases
- All dependencies bundled (no version conflicts)
- Working xdg-desktop-portal-hyprland

## Build Locally

Requirements:
```bash
sudo dnf install docker rpm-build
```

Build:
```bash
git clone https://github.com/asherbuk/Hyprland-Fedora
cd Hyprland-Fedora

# Option 1: Build RPM (recommended)
./build-rpm.sh
sudo dnf install ./output/hyprland-*.rpm

# Option 2: Docker only (binaries without packaging)
./build-fedora43.sh
```

## Update

```bash
git pull
./build-rpm.sh
sudo dnf upgrade ./output/hyprland-*.rpm
```

Or wait for COPR to auto-update (webhook triggers on new tags).

## Remove

```bash
sudo dnf remove hyprland
sudo dnf copr disable asherbuk/hyprland
```

## After Install

Re-login and verify:

```bash
Hyprland --version
systemctl --user status xdg-desktop-portal-hyprland
```

## Files

| File | Purpose |
|------|---------|
| `Dockerfile.fedora43` | Docker build environment |
| `build-fedora43.sh` | Build binaries via Docker |
| `build-rpm.sh` | Package binaries into RPM |
| `hyprland.spec` | RPM spec (local builds) |
| `hyprland-copr.spec` | RPM spec (COPR builds) |

## COPR Setup

This repo uses COPR webhook for automatic builds:

1. Fork is tagged with new version
2. Webhook triggers COPR build
3. Users get update via `dnf upgrade`

---

## Maintenance Status

**Active** - Updates when I need the latest version myself.

## License

Hyprland is BSD-3-Clause. Build scripts in this repo are MIT.
