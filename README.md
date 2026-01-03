# Hyprland 0.53↑ for Fedora

[![Copr build status](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/package/hyprland/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/)

**Latest stable Hyprland releases for Fedora, built with modern packaging approach.**

> This is a **personal COPR repository**, not an official Fedora package!  
> Maintained for personal use and provided as-is.

Source: [fedora-build/hyprland-copr.spec](fedora-build/hyprland-copr.spec) core compositor,

[fedora-build/xdg-desktop-portal-hyprland.spec](fedora-build/xdg-desktop-portal-hyprland.spec) portal spec.

Follows **hermetic build principles**:

- **Vendored dependencies** — all Hyprland-specific libraries built from pinned versions
- **RPATH isolation** — libraries in `/usr/libexec/hyprland/vendor/`, no `LD_LIBRARY_PATH` hacks
- **Zero ABI conflicts** — no version collisions with system or other COPR packages
- **Reproducible builds** — same source, same result.

### Why This Repo?

Fedora 43 does not ship Hyprland in official repositories. Existing COPRs rely on external package dependencies which can break on version mismatches.

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

<img width="2240" height="1400" alt="hypr-f43" src="https://github.com/user-attachments/assets/6fad5b0a-1be1-4d72-8231-8a6ee03aff5c" />

### What's Included

| Package | Description |
|---------|-------------|
| `hyprland` | Dynamic tiling Wayland compositor (`Hyprland`, `hyprctl`, `hyprpm`, `start-hyprland`) |
| `xdg-desktop-portal-hyprland` | Portal backend for screen sharing, file dialogs |

**Vendored libraries** (in `/usr/libexec/hyprland/vendor/`):

libaquamarine, libhyprlang, libhyprutils, libhyprcursor, libhyprgraphics, libhyprwire

## Build Details

- Libraries installed to private prefix (`/usr/libexec/hyprland/vendor/`)
- RPATH set at build time via CMake (not patchelf — avoids ELF corruption)
- System libraries (wayland, mesa, libinput) from Fedora repos

## License

- **Hyprland** and libraries: **BSD-3-Clause** (upstream)
- **Build specs and scripts** are **MIT**

## Links

- [COPR Repository](https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/)
- [Upstream Hyprland](https://github.com/hyprwm/Hyprland)
- [Hyprland Wiki](https://wiki.hyprland.org/)
- [Tech write-up](https://ashbuk.hashnode.dev/hyprland-fedora)

---

[![Sponsor](https://img.shields.io/badge/Sponsor-💖-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/AshBuk) [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=R3HZH8DX7SCJG)
