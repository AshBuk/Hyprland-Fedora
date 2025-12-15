#!/bin/bash
# Build Hyprland 0.52+ and xdg-desktop-portal-hyprland for Fedora 43

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/output"
IMAGE_NAME="hyprland-fedora43"

echo "=== Building Hyprland + xdg-desktop-portal-hyprland for Fedora 43 ==="
echo "Output directory: ${OUTPUT_DIR}"

# Create output directory
mkdir -p "${OUTPUT_DIR}"

# Build Docker image
echo ""
echo "=== Building Docker image... ==="
docker build -f "${SCRIPT_DIR}/../Dockerfile.fedora43" -t "${IMAGE_NAME}" "${SCRIPT_DIR}/.."

# Extract artifacts
echo ""
echo "=== Extracting build artifacts... ==="
docker run --rm -v "${OUTPUT_DIR}:/output" "${IMAGE_NAME}"

echo ""
echo "=== Build complete! ==="
echo "Artifacts location: ${OUTPUT_DIR}"
echo ""
echo "Files:"
ls -la "${OUTPUT_DIR}"
echo ""
echo "To install manually:"
echo "  sudo cp ${OUTPUT_DIR}/Hyprland /usr/local/bin/"
echo "  sudo cp ${OUTPUT_DIR}/hyprctl /usr/local/bin/"
echo "  sudo cp ${OUTPUT_DIR}/hyprpm /usr/local/bin/"
echo "  sudo cp ${OUTPUT_DIR}/xdg-desktop-portal-hyprland /usr/libexec/"
echo "  sudo cp ${OUTPUT_DIR}/hyprland-share-picker /usr/bin/"
echo ""
echo "Portal files:"
echo "  sudo cp ${OUTPUT_DIR}/portal-data/hyprland.portal /usr/share/xdg-desktop-portal/portals/"
echo "  sudo cp ${OUTPUT_DIR}/portal-data/org.freedesktop.impl.portal.desktop.hyprland.service /usr/share/dbus-1/services/"
echo "  sudo cp ${OUTPUT_DIR}/portal-data/xdg-desktop-portal-hyprland.service /usr/lib/systemd/user/"
