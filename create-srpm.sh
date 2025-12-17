#!/bin/bash
# Create SRPM for COPR submission
set -e

VERSION="0.52.2"
RELEASE="1"

# Dependency versions (must match spec file)
HYPRLAND_PROTOCOLS_VER="0.6.4"
UDIS86_VER="1.7.2"
HYPRWAYLAND_SCANNER_VER="0.4.5"
HYPRUTILS_VER="0.11.0"
HYPRLANG_VER="0.6.7"
HYPRCURSOR_VER="0.1.13"
HYPRGRAPHICS_VER="0.4.0"
AQUAMARINE_VER="0.10.0"

echo "=== Creating SRPM for Hyprland ${VERSION} ==="

mkdir -p sources
cd sources

# Download main source
if [ ! -f "hyprland-${VERSION}.tar.gz" ]; then
    echo "Downloading Hyprland source..."
    curl -L -o "hyprland-${VERSION}.tar.gz" \
         "https://github.com/hyprwm/Hyprland/archive/refs/tags/v${VERSION}.tar.gz"
fi

# Download submodules
if [ ! -f "hyprland-protocols-${HYPRLAND_PROTOCOLS_VER}.tar.gz" ]; then
    echo "Downloading hyprland-protocols..."
    curl -L -o "hyprland-protocols-${HYPRLAND_PROTOCOLS_VER}.tar.gz" \
         "https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v${HYPRLAND_PROTOCOLS_VER}.tar.gz"
fi

if [ ! -f "udis86-${UDIS86_VER}.tar.gz" ]; then
    echo "Downloading udis86..."
    curl -L -o "udis86-${UDIS86_VER}.tar.gz" \
         "https://github.com/canihavesomecoffee/udis86/archive/refs/tags/v${UDIS86_VER}.tar.gz"
fi

# Download dependencies
if [ ! -f "hyprwayland-scanner-${HYPRWAYLAND_SCANNER_VER}.tar.gz" ]; then
    echo "Downloading hyprwayland-scanner..."
    curl -L -o "hyprwayland-scanner-${HYPRWAYLAND_SCANNER_VER}.tar.gz" \
         "https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v${HYPRWAYLAND_SCANNER_VER}.tar.gz"
fi

if [ ! -f "hyprutils-${HYPRUTILS_VER}.tar.gz" ]; then
    echo "Downloading hyprutils..."
    curl -L -o "hyprutils-${HYPRUTILS_VER}.tar.gz" \
         "https://github.com/hyprwm/hyprutils/archive/refs/tags/v${HYPRUTILS_VER}.tar.gz"
fi

if [ ! -f "hyprlang-${HYPRLANG_VER}.tar.gz" ]; then
    echo "Downloading hyprlang..."
    curl -L -o "hyprlang-${HYPRLANG_VER}.tar.gz" \
         "https://github.com/hyprwm/hyprlang/archive/refs/tags/v${HYPRLANG_VER}.tar.gz"
fi

if [ ! -f "hyprcursor-${HYPRCURSOR_VER}.tar.gz" ]; then
    echo "Downloading hyprcursor..."
    curl -L -o "hyprcursor-${HYPRCURSOR_VER}.tar.gz" \
         "https://github.com/hyprwm/hyprcursor/archive/refs/tags/v${HYPRCURSOR_VER}.tar.gz"
fi

if [ ! -f "hyprgraphics-${HYPRGRAPHICS_VER}.tar.gz" ]; then
    echo "Downloading hyprgraphics..."
    curl -L -o "hyprgraphics-${HYPRGRAPHICS_VER}.tar.gz" \
         "https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v${HYPRGRAPHICS_VER}.tar.gz"
fi

if [ ! -f "aquamarine-${AQUAMARINE_VER}.tar.gz" ]; then
    echo "Downloading aquamarine..."
    curl -L -o "aquamarine-${AQUAMARINE_VER}.tar.gz" \
         "https://github.com/hyprwm/aquamarine/archive/refs/tags/v${AQUAMARINE_VER}.tar.gz"
fi

cd ..

# Create SRPM
echo "Creating SRPM..."
mkdir -p srpm

rpmbuild -bs hyprland-copr.spec \
         --define "_sourcedir $(pwd)/sources" \
         --define "_srcrpmdir $(pwd)/srpm" \
         --define "dist .fc43"

echo ""
echo "=== SRPM created successfully! ==="
echo "Location: $(pwd)/srpm/"
ls -la srpm/*.src.rpm 2>/dev/null || echo "No SRPM found"
echo ""
echo "To submit to COPR:"
echo "  copr-cli build ashbuk/Hyprland-Fedora srpm/hyprland-${VERSION}-${RELEASE}.fc43.src.rpm"
