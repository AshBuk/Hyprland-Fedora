#!/bin/bash
# Copyright (c) 2025 Asher Buk
# SPDX-License-Identifier: MIT
# https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/
#
# Create SRPMs for COPR submission
# Usage: ./create-srpm.sh [spec...]
#   No arguments: builds all spec files
#   With arguments: builds only specified specs (e.g. ./create-srpm.sh hyprland-copr.spec)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HYPRLAND_SPEC="$SCRIPT_DIR/hyprland-copr.spec"

# =============================================================================
# Parse versions from spec files
# =============================================================================
parse_spec_global() {
    local spec="$1" key="$2"
    grep -oP "^%global ${key}\\s+\\K\\S+" "$spec" || true
}

# Hyprland main spec is the source of truth for shared vendored lib versions
HYPRLAND_VERSION=$(parse_spec_global "$HYPRLAND_SPEC" "hyprland_version")
HYPRLAND_PROTOCOLS_VER=$(parse_spec_global "$HYPRLAND_SPEC" "hyprland_protocols_ver")
HYPRWAYLAND_SCANNER_VER=$(parse_spec_global "$HYPRLAND_SPEC" "hyprwayland_scanner_ver")
HYPRUTILS_VER=$(parse_spec_global "$HYPRLAND_SPEC" "hyprutils_ver")
HYPRLANG_VER=$(parse_spec_global "$HYPRLAND_SPEC" "hyprlang_ver")
HYPRCURSOR_VER=$(parse_spec_global "$HYPRLAND_SPEC" "hyprcursor_ver")
HYPRGRAPHICS_VER=$(parse_spec_global "$HYPRLAND_SPEC" "hyprgraphics_ver")
AQUAMARINE_VER=$(parse_spec_global "$HYPRLAND_SPEC" "aquamarine_ver")
HYPRWIRE_VER=$(parse_spec_global "$HYPRLAND_SPEC" "hyprwire_ver")
GLAZE_VER=$(parse_spec_global "$HYPRLAND_SPEC" "glaze_ver")
BUILD_ASSETS_RELEASE=$(parse_spec_global "$HYPRLAND_SPEC" "build_assets_release")

# Subpackage versions (in hyprland-copr.spec)
HYPRLOCK_VERSION=$(parse_spec_global "$HYPRLAND_SPEC" "hyprlock_version")
HYPRIDLE_VERSION=$(parse_spec_global "$HYPRLAND_SPEC" "hypridle_version")

# Satellite package versions (separate specs)
PORTAL_VERSION=$(parse_spec_global "$SCRIPT_DIR/xdg-desktop-portal-hyprland.spec" "portal_version")

# =============================================================================
# Validate vendored dep versions in satellite specs
# =============================================================================
validate_version() {
    local spec="$1" key="$2" expected="$3"
    local actual
    actual=$(parse_spec_global "$spec" "$key")
    if [ -n "$actual" ] && [ "$actual" != "$expected" ]; then
        echo "ERROR: $(basename "$spec") has $key=$actual, expected $expected (from hyprland-copr.spec)"
        exit 1
    fi
}

echo "=== Validating vendored dep versions ==="
SATELLITE_SPEC="$SCRIPT_DIR/xdg-desktop-portal-hyprland.spec"
validate_version "$SATELLITE_SPEC" "hyprwayland_scanner_ver" "$HYPRWAYLAND_SCANNER_VER"
validate_version "$SATELLITE_SPEC" "hyprutils_ver"           "$HYPRUTILS_VER"
validate_version "$SATELLITE_SPEC" "hyprlang_ver"            "$HYPRLANG_VER"
validate_version "$SATELLITE_SPEC" "hyprcursor_ver"          "$HYPRCURSOR_VER"
validate_version "$SATELLITE_SPEC" "hyprgraphics_ver"        "$HYPRGRAPHICS_VER"
validate_version "$SATELLITE_SPEC" "hyprland_protocols_ver"  "$HYPRLAND_PROTOCOLS_VER"
echo "  All versions consistent with hyprland-copr.spec"

# =============================================================================
# Download helper
# =============================================================================
download() {
    local file="$1" url="$2"
    if [ ! -f "$file" ]; then
        echo "  Downloading $file..."
        curl -L -o "$file" "$url"
    fi
}

# =============================================================================
# Download sources
# =============================================================================
echo "=== Downloading sources ==="
mkdir -p sources
cd sources

# --- Main package sources (includes subpackages hyprlock, hypridle) ---
download "hyprland-${HYPRLAND_VERSION}.tar.gz" \
    "https://github.com/hyprwm/Hyprland/archive/refs/tags/v${HYPRLAND_VERSION}.tar.gz"
download "udis86-hyprland.tar.gz" \
    "https://github.com/AshBuk/Hyprland-Fedora/releases/download/${BUILD_ASSETS_RELEASE}/udis86-hyprland.tar.gz"
download "glaze-${GLAZE_VER}.tar.gz" \
    "https://github.com/stephenberry/glaze/archive/refs/tags/v${GLAZE_VER}.tar.gz"
download "hyprlock-${HYPRLOCK_VERSION}.tar.gz" \
    "https://github.com/hyprwm/hyprlock/archive/refs/tags/v${HYPRLOCK_VERSION}.tar.gz"
download "hypridle-${HYPRIDLE_VERSION}.tar.gz" \
    "https://github.com/hyprwm/hypridle/archive/refs/tags/v${HYPRIDLE_VERSION}.tar.gz"

# --- Satellite package sources ---
download "xdg-desktop-portal-hyprland-${PORTAL_VERSION}.tar.gz" \
    "https://github.com/hyprwm/xdg-desktop-portal-hyprland/archive/refs/tags/v${PORTAL_VERSION}.tar.gz"

# --- Shared vendored dependencies (used by multiple specs) ---
download "hyprland-protocols-${HYPRLAND_PROTOCOLS_VER}.tar.gz" \
    "https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v${HYPRLAND_PROTOCOLS_VER}.tar.gz"
download "hyprwayland-scanner-${HYPRWAYLAND_SCANNER_VER}.tar.gz" \
    "https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v${HYPRWAYLAND_SCANNER_VER}.tar.gz"
download "hyprutils-${HYPRUTILS_VER}.tar.gz" \
    "https://github.com/hyprwm/hyprutils/archive/refs/tags/v${HYPRUTILS_VER}.tar.gz"
download "hyprlang-${HYPRLANG_VER}.tar.gz" \
    "https://github.com/hyprwm/hyprlang/archive/refs/tags/v${HYPRLANG_VER}.tar.gz"
download "hyprcursor-${HYPRCURSOR_VER}.tar.gz" \
    "https://github.com/hyprwm/hyprcursor/archive/refs/tags/v${HYPRCURSOR_VER}.tar.gz"
download "hyprgraphics-${HYPRGRAPHICS_VER}.tar.gz" \
    "https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v${HYPRGRAPHICS_VER}.tar.gz"
download "aquamarine-${AQUAMARINE_VER}.tar.gz" \
    "https://github.com/hyprwm/aquamarine/archive/refs/tags/v${AQUAMARINE_VER}.tar.gz"
download "hyprwire-${HYPRWIRE_VER}.tar.gz" \
    "https://github.com/hyprwm/hyprwire/archive/refs/tags/v${HYPRWIRE_VER}.tar.gz"

cd ..

# =============================================================================
# Build SRPMs
# =============================================================================
# Determine which specs to build
if [ $# -gt 0 ]; then
    SPECS=("$@")
else
    SPECS=(hyprland-copr.spec xdg-desktop-portal-hyprland.spec)
fi

echo ""
echo "=== Creating SRPMs ==="
mkdir -p srpm

for spec in "${SPECS[@]}"; do
    if [ ! -f "$spec" ]; then
        echo "ERROR: $spec not found, skipping"
        continue
    fi
    echo "  Building SRPM from $spec..."
    rpmbuild -bs "$spec" \
             --define "_sourcedir $(pwd)/sources" \
             --define "_srcrpmdir $(pwd)/srpm" \
             --define "dist .fc43"
done

echo ""
echo "=== SRPMs created successfully! ==="
echo "Location: $(pwd)/srpm/"
ls -la srpm/*.src.rpm 2>/dev/null || echo "No SRPMs found"
