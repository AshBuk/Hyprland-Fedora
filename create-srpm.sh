#!/bin/bash
# Copyright (c) 2025 Asher Buk
# SPDX-License-Identifier: MIT
# https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/
#
# Create SRPM for COPR submission
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SPEC_FILE="$SCRIPT_DIR/hyprland-copr.spec"

# =============================================================================
# Parse versions from spec file (single source of truth)
# =============================================================================
parse_spec_global() {
    grep -oP "^%global $1\\s+\\K\\S+" "$SPEC_FILE"
}

VERSION=$(parse_spec_global "hyprland_version")
RELEASE=$(grep -oP '^Release:\s+\K[0-9]+' "$SPEC_FILE")
HYPRLAND_PROTOCOLS_VER=$(parse_spec_global "hyprland_protocols_ver")
HYPRWAYLAND_SCANNER_VER=$(parse_spec_global "hyprwayland_scanner_ver")
HYPRUTILS_VER=$(parse_spec_global "hyprutils_ver")
HYPRLANG_VER=$(parse_spec_global "hyprlang_ver")
HYPRCURSOR_VER=$(parse_spec_global "hyprcursor_ver")
HYPRGRAPHICS_VER=$(parse_spec_global "hyprgraphics_ver")
AQUAMARINE_VER=$(parse_spec_global "aquamarine_ver")
HYPRWIRE_VER=$(parse_spec_global "hyprwire_ver")
GLAZE_VER=$(parse_spec_global "glaze_ver")

echo "=== Creating SRPM for Hyprland ${VERSION} ==="
echo "Versions parsed from: $(basename "$SPEC_FILE")"

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

# udis86: use local subproject (patched for Python 3.x, includes CMakeLists.txt)
if [ ! -f "udis86-hyprland.tar.gz" ]; then
    echo "Creating udis86 tarball from local subproject..."
    (cd "$REPO_ROOT/subprojects" && tar -czvf "$SCRIPT_DIR/sources/udis86-hyprland.tar.gz" udis86)
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

# NEW: hyprwire IPC library
if [ ! -f "hyprwire-${HYPRWIRE_VER}.tar.gz" ]; then
    echo "Downloading hyprwire..."
    curl -L -o "hyprwire-${HYPRWIRE_VER}.tar.gz" \
         "https://github.com/hyprwm/hyprwire/archive/refs/tags/v${HYPRWIRE_VER}.tar.gz"
fi

# glaze: for hyprpm (mock chroot has no network for FetchContent)
if [ ! -f "glaze-${GLAZE_VER}.tar.gz" ]; then
    echo "Downloading glaze..."
    curl -L -o "glaze-${GLAZE_VER}.tar.gz" \
         "https://github.com/stephenberry/glaze/archive/refs/tags/v${GLAZE_VER}.tar.gz"
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
