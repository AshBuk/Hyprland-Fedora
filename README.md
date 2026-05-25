# Hyprland for Fedora

[![Copr build status](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/package/hyprland/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/)

**Latest stable Hyprland releases for Fedora, built with modern packaging approach.**

> This is a **personal COPR repository**, not an official Fedora package!  
> Maintained for personal use and provided as-is.

Source: [hyprland-copr.spec](hyprland-copr.spec) compositor + hyprlock + hypridle,
[xdg-desktop-portal-hyprland.spec](xdg-desktop-portal-hyprland.spec) portal spec.

Follows **hermetic build principles**:

- **Vendored dependencies** — all Hyprland-specific libraries built from pinned versions
- **RPATH isolation** — libraries in `/usr/libexec/hyprland/vendor/`, no `LD_LIBRARY_PATH` hacks
- **Zero ABI conflicts** — no version collisions with system or other COPR packages
- **Reproducible builds** — same source, same result.

### Why This Repo?

Fedora 43/44 does not ship Hyprland in official repositories. Existing COPRs rely on external package dependencies which can break on version mismatches.

**Technical guarantees:**

- Latest stable Hyprland (updated manually, not auto-tracking git HEAD)
- Self-contained builds with no external hypr-* package dependencies
- Clean `dnf repoquery --duplicates` — no parallel-install conflicts

### Quick Start

```bash
# Install
sudo dnf copr enable ashbuk/Hyprland-Fedora
sudo dnf install hyprland

# Screen sharing support (recommended)
sudo dnf install xdg-desktop-portal-hyprland

# Update
sudo dnf upgrade hyprland

# Remove
sudo dnf remove hyprland xdg-desktop-portal-hyprland
sudo dnf copr disable ashbuk/Hyprland-Fedora
```

![hyprland-fedora](https://github.com/user-attachments/assets/d6ddaaaa-4964-4804-a2f5-5d9c1f816c6b)

### What's Included

| Package | Description |
|---------|-------------|
| `hyprland` | Dynamic tiling Wayland compositor (`Hyprland`, `hyprctl`, `hyprpm`, `start-hyprland`) |
| `hyprlock` | Screen lock utility (subpackage, installed with hyprland) |
| `hypridle` | Idle daemon for lock/sleep on inactivity (subpackage, installed with hyprland) |
| `xdg-desktop-portal-hyprland` | Portal backend for screen sharing, file dialogs |

**Vendored libraries** (in `/usr/libexec/hyprland/vendor/`):

libaquamarine, libhyprlang, libhyprutils, libhyprcursor, libhyprgraphics, libhyprwire, hyprwayland-scanner, hyprland-protocols, udis86, glaze

## Build Details

- Libraries installed to private prefix (`/usr/libexec/hyprland/vendor/`)
- RPATH set at build time via CMake (not patchelf — avoids ELF corruption)
- System libraries (wayland, mesa, libinput) from Fedora repos

**License: Build specs and scripts** are **[MIT](https://github.com/AshBuk/Hyprland-Fedora?tab=MIT-1-ov-file)**

## Links

- [COPR Repository](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/)
- [Upstream Hyprland](https://github.com/hyprwm/Hyprland)
- [Hyprland Wiki](https://wiki.hyprland.org/)
- [Article](https://ashbuk.dev/posts/hyprland-055/)

---

[![Sponsor](https://img.shields.io/badge/Sponsor-💖-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/AshBuk) [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=R3HZH8DX7SCJG)
