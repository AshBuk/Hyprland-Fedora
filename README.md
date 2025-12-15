# Hyprland for Fedora 43+

[![Copr build status](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/package/hyprland/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/)

Hyprland builds for Fedora 43 with the latest upstream features.

> ⚠️ **Disclaimer**  
> This is a **personal COPR repository**, not an official Fedora package.  
> It is maintained for personal use and provided as-is.

## Why This Repo?

Fedora 43 ships with Hyprland **0.45**, while upstream is already at **0.52+**.

I built this primarily for myself, because I need newer compositor features that are not available in:
- the official Fedora repositories
- the existing COPR at  
  https://github.com/solopasha/hyprlandRPM

This repository provides:

- Latest Hyprland releases
- All required dependencies bundled (no version conflicts)
- Working `xdg-desktop-portal-hyprland`

## Install from COPR (copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora)
https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/

```bash
sudo dnf copr enable ashbuk/Hyprland-Fedora
sudo dnf install hyprland
```

**re-login and verify:**

```bash
Hyprland --version
systemctl --user status xdg-desktop-portal-hyprland
```

## What's Included

| Package | Description |
|--------|-------------|
| hyprland | Dynamic tiling Wayland compositor |
| hyprctl | CLI control tool |
| hyprpm | Plugin manager |
| xdg-desktop-portal-hyprland | Screen sharing portal |
| hyprland-libs | hyprlang, hyprutils, hyprcursor, hyprgraphics, aquamarine |

## Update

Packages are updated automatically via COPR when new tags are pushed.

```bash
sudo dnf upgrade hyprland
```

## Remove

```bash 
sudo dnf remove hyprland
sudo dnf copr disable ashbuk/Hyprland-Fedora
```